# -*- coding: utf-8 -*-
# 对数据库中的代理IP进行定期检测，检测到可用的放入缓存中备用
import os
import socket
import requests
import urllib
import time
from bs4 import BeautifulSoup

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
def checkIpProxy(ip, prot):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    url = "https://blog.csdn.net/?s=123132123"
    proxy_dict = {
        "http": "http://" + ip + ":" + str(prot)
    }

    proxy_info = {'host': ip,
                  'port': prot
                  }
    proxy_support = urllib.request.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
    # proxy_support = urllib.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url, headers=headers)
    htmlpage = urllib.request.urlopen(request).read(200000)
    soup = BeautifulSoup(htmlpage, "lxml")
    return soup.title


def user_proxy(proxy_addr, url):
    import urllib.request
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data


if __name__ == '__main__':
    print(getCurrIp())
    print(getCurrIp())
    print(getCurrIp())
# sched.start()
