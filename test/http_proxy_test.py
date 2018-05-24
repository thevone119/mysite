# -*- coding: utf-8 -*-
import requests
import random

def testProxy(host,url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    proxy = 'http://' + host
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
    r = requests.get(url, headers=headers, proxies=proxies, allow_redirects=True)
    r.encoding = "GBK"
    print(r.text)

def _randomIp():
    return str(random.randint(14, 150))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255))

if __name__ == '__main__':
    for i in range(1):
        print(_randomIp())
    #testProxy("218.0.68.205:24102", url = "https://ip.cn/")

    testProxy("60.168.11.90:20003", url="https://shop.taobao.com/getShopInfo.htm?shopId=1971&staobaoz_20180523&rd=1527072243.0714676")