# -*- coding: utf-8 -*-
# 对数据库中的代理IP进行定期检测，检测到可用的放入缓存中备用
import os
import socket
import requests
import django
import time
from mysite.libs import myredis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
django.setup()  # 执行
# 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
from mysite.app.ipproxy import models

# 当前的外网ip的全局变量(每10分钟重新检测一次)
currip = ""
# 最后检测时间，全局变量
last_updata_ip = 0.1


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


# 获取当前的ip(外网的ip)
def getCurrIp():
    global currip
    global last_updata_ip
    if len(currip) > 2 and (time.time() - last_updata_ip) < 60 * 10:
        return currip
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    print("getCurrIp--")
    url = "http://2017.ip138.com/ic.asp"
    r = requests.get(url, headers=headers)
    ip = r.text[r.text.find("[") + 1:r.text.find("]")]
    if len(ip) > 5:
        currip = ip
        last_updata_ip = time.time()
    return currip


# 校验代理是否可以用
def checkIpProxy(prol,ip, prot):
    try:
        cip = getCurrIp()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        proxies = {
            prol: "http://" + ip + ":" + str(prot)
        }
        url = "http://2017.ip138.com/ic.asp"
        r = requests.get(url, headers=headers, proxies=proxies)
        ip = r.text[r.text.find("[") + 1:r.text.find("]")]
        print(ip)
        if len(ip)<3:
            return False
        if ip != cip:
            return True
    except Exception:
        pass
    return False

#加载有效的ip，匿名的ip到缓存中
def loadActiveIp():
    #只查询最近5分钟的
    mintime = int(time.time()*1000)-1000*60*10

    iplist = models.TIpProxy.objects.filter(update_time__gt=mintime).order_by("-update_time").all()
    print(len(iplist))
    for ipm in iplist:
        if checkIpCon(ipm.ip,ipm.prot):
            pass
        else:
            continue
        if checkIpProxy(ipm.protocol,ipm.ip,ipm.prot):
            print(ipm)



    pass




if __name__ == '__main__':
    #死循环，一直检测ip是否可用
    while True:
        loadActiveIp()
        time.sleep(3)
# sched.start()
