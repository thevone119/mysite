# -*- coding: utf-8 -*-
import socket
import threading
import requests
import time
from mysite.libs import stringExt
from mysite.app.ipproxy import models

# 当前的外网ip的全局变量(每10分钟重新检测一次)
currip = ""
# 最后检测时间，全局变量
last_updata_ip = 0.1
# 引入锁
L = threading.Lock()

# 校验IP，端口是否可用
def checkIpCon(ipm=None):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)
    h = ipm.host.split(":")
    if(len(h)!=2):
        return False
    ip = h[0]
    prot = int(h[1])
    try:
        sk.connect((ip, prot))
        return True
    except Exception as e:
        print(e)
        pass
    finally:
        sk.close()
    return False

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
        proxy = 'http://'+ipm.host
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        # 忽略警告
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, proxies=proxies, headers=headers, allow_redirects=False, verify=False)
        r.encoding = 'utf-8'
        ip = stringExt.ExtStr(r.text, "IP：<code>", "</code>")
        print("getip:"+ip)
        if len(ip) < 3 or len(ip)>20:
            return False
        if ip != cip:
            return True
    except Exception:
        pass
    return False

if __name__ == '__main__':

    ipm=models.TIpProxy()
    ipm.host = "127.0.0.1:3333"
    print(checkIpCon(ipm))