# -*- coding: utf-8 -*-
# 对数据库中的代理IP进行定期检测，检测到可用的放入缓存中备用
import os
import socket
import requests
import django
import time
import threading
import urllib.request
from mysite.libs import stringExt
from mysite.libs import MyThreadPool

from mysite.libs import myredis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
django.setup()  # 执行
# 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
from mysite.app.ipproxy import models

# 当前的外网ip的全局变量(每10分钟重新检测一次)
currip = ""
# 最后检测时间，全局变量
last_updata_ip = 0.1
# 引入锁
L = threading.Lock()


# 校验IP，端口是否可用
def checkIpCon(ip, prot):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)
    try:
        sk.connect((ip, prot))
        return True
    except Exception:

        pass
    sk.close()
    return False


def httpRequest(url, proxy=None, type='http', chart='utf-8'):
    try:
        ret = None
        SockFile = None
        request = urllib.request.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3')
        request.add_header('Pragma', 'no-cache')
        print(proxy)
        if proxy:
            request.set_proxy(proxy, type)
        opener = urllib.request.build_opener()
        SockFile = opener.open(request)
        ret = SockFile.read().decode(chart)
    finally:
        if SockFile:
            SockFile.close()

    return ret


# 获取当前的ip(外网的ip)
def getCurrIp():
    L.acquire()
    global currip
    global last_updata_ip
    try:
        if len(currip) > 2 and (time.time() - last_updata_ip) < 60 * 10:
            return currip
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'
        }
        print("getCurrIp--")
        # 忽略警告
        requests.packages.urllib3.disable_warnings()
        url = "https://ip.cn/"
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        ip = stringExt.ExtStr(r.text, "IP：<code>", "</code>")
        if len(ip) > 5 and len(ip) < 20:
            currip = ip
            last_updata_ip = time.time()
        pass
    except Exception:
        pass
    finally:
        L.release()
    return currip


# 校验代理是否可以用
def checkIpProxy(ipm=None):
    try:
        cip = getCurrIp()

        url = "https://ip.cn/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'
        }
        proxy = 'http://' + ipm.host
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        # 忽略警告
        requests.packages.urllib3.disable_warnings()
        url = "https://ip.cn/"
        r = requests.get(url, proxies=proxies, headers=headers, allow_redirects=False, verify=False)
        r.encoding = 'utf-8'
        ip = stringExt.ExtStr(r.text, "IP：<code>", "</code>")
        print("getip:"+ip)
        if len(ip) < 3 or len(ip)>20:
            return False
        if ip != cip:
            print("update")
            ipm.check_time = int(time.time())
            ipm.save()
            #ipm.update(check_time=int(time.time()))
            return True
    except Exception:
        pass
    return False


# 加载有效的ip，匿名的ip到缓存中
def loadActiveIp():
    # 只查询最近5分钟的
    mintime = int(time.time() * 1000) - 1000 * 60 * 300
    pool = MyThreadPool.MyThreadPool(8)

    #iplist = models.TIpProxy.objects.filter(update_time__gt=mintime).order_by("-update_time").all()[:500]
    iplist = models.TIpProxy.objects.order_by("-update_time").all()[:500]
    print(len(iplist))
    for ipm in iplist:
        pool.callInThread(checkIpProxy, ipm)

    pass


if __name__ == '__main__':
    # 死循环，一直检测ip是否可用
    while True:
        loadActiveIp()
        time.sleep(3)
# sched.start()
