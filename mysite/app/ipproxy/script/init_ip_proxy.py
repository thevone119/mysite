# -*- coding: utf-8 -*-
# 把所有代理IP信息进行抓取，然后存储到数据库中，每5分钟进行一次抓取
# 1.所有代理ip抓取成功后，把ip放入redis缓存池中
# 2.定时从缓存池中取出ip，验证是否可用代理，如果是可用代理，则放入可用代理池中
# 3.

import json
import requests
from bs4 import BeautifulSoup
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from mysite.app.ipproxy import ippool
from mysite.app.ipproxy import models
from mysite.app.ipproxy import ipcommon
from mysite.libs import MyThreadPool



sched = BlockingScheduler()

# 抓取西刺代理的数据每5分钟执行一次
# http://www.xicidaili.com/nn/27
@sched.scheduled_job('interval', minutes=5)
def xici_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    for i in range(1, 10):
        url = "http://www.xicidaili.com/nn/" + str(i)
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")开始-----")
        r = requests.get(url, headers=headers)
        r.enconding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        trs = soup.find_all("tr")
        for tr in trs[1:]:
            txt = tr.text
            if txt.find("HTTP") < 0:
                continue
            tline = txt.split("\n")
            ud = str(int(time.time() * 1000))
            ipm = models.TIpProxy(update_time=ud)
            ipm.src_url = url
            idx = 0
            qip = ""
            qprot = ""
            for l in tline:
                l = l.strip()
                if len(l) < 1:
                    continue
                if idx == 0:
                    qip = l
                if idx == 1:
                    qprot = l
                    pass
                if idx == 2:
                    ipm.loc = l
                if idx == 3:
                    ipm.proxy_type = getproxyType(l)
                if idx == 4:
                    ipm.protocol = l
                idx = idx + 1
            ipm.host = qip + ":" + qprot
            ippool.pushNoCheckIp(ipm)
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")
    pass


# 抓取快代理数据，5分钟一次
# https://www.kuaidaili.com/free/inha/2/
@sched.scheduled_job('interval', minutes=5)
def kuaidaili_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    for i in range(1, 10):
        url = "https://www.kuaidaili.com/free/inha/" + str(i)
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")开始-----")
        r = requests.get(url, headers=headers)
        r.enconding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        trs = soup.find_all("tr")
        for tr in trs[1:]:
            txt = tr.text
            if txt.find("HTTP") < 0:
                continue
            tline = txt.split("\n")
            ud = str(int(time.time() * 1000))
            ipm = models.TIpProxy(update_time=ud)
            ipm.src_url = url
            idx = 0
            qip = ""
            qprot = ""
            for l in tline:
                l = l.strip()
                if len(l) < 1:
                    continue
                if idx == 0:
                    qip = l
                if idx == 1:
                    qprot = l
                    pass
                if idx == 4:
                    ipm.loc = l
                if idx == 2:
                    ipm.proxy_type = getproxyType(l)
                if idx == 3:
                    ipm.protocol = l
                idx = idx + 1
            ipm.host = qip + ":" + qprot
            ippool.pushNoCheckIp(ipm)
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")
    pass


# 抓取data5u代理数据，1分钟一次
# http://www.data5u.com/free/gngn/index.shtml
@sched.scheduled_job('interval', minutes=5)
def data5u_query():
    data5u_query_url("http://www.data5u.com/free/gngn/index.shtml")
    data5u_query_url("http://www.data5u.com/free/gwgn/index.shtml")


def data5u_query_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    # url = "http://www.data5u.com/free/gngn/index.shtml"
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站（", url, ")开始-----")
    r = requests.get(url, headers=headers)
    r.enconding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.find_all("ul", attrs={'class': ['l2']})
    for tr in trs[1:]:
        txt = tr.text
        if txt.find("http") < 0:
            continue
        tline = txt.split("\n")
        ud = str(int(time.time() * 1000))
        ipm = models.TIpProxy(update_time=ud)
        ipm.src_url = url
        idx = 0
        qip = ""
        qprot = ""
        for l in tline:
            l = l.strip()

            if len(l) < 1:
                continue
            if idx == 0:
                qip = l
            if idx == 1:
                qprot = l
                pass
            if idx == 4:
                ipm.loc = l
            if idx == 2:
                ipm.proxy_type = getproxyType(l)
            if idx == 3:
                ipm.protocol = l
            idx = idx + 1
        ipm.host = qip + ":" + qprot
        ippool.pushNoCheckIp(ipm)

    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站（", url, ")结束-----")
    pass


# 抓取熊猫代理数据，5分钟一次
# http://www.xiongmaodaili.com/xiongmao-web/freeip/list
@sched.scheduled_job('interval', minutes=1)
def xiongmaodaili_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    url = "http://www.xiongmaodaili.com/xiongmao-web/freeip/list"
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")开始-----")
    r = requests.get(url, headers=headers)
    r.enconding = "utf-8"
    js = json.loads(r.text)
    if js["code"] != '0':
        return
        pass
    list = js['obj']
    for lj in list:
        ud = str(int(time.time() * 1000))
        ipm = models.TIpProxy(update_time=ud)
        ipm.src_url = url
        ipm.host = lj['ip']+":"+str(lj['port'])
        ipm.protocol = "HTTPS"
        ipm.proxy_type = 2
        ipm.loc = lj['addr']
        ippool.pushNoCheckIp(ipm)
    pass
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")


# 抓取66ip代理数据，5分钟一次
# http://www.66ip.cn/
@sched.scheduled_job('interval', seconds=60)
def ip66_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    url = "http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip"
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")开始-----")
    r = requests.get(url, headers=headers, timeout=5)
    r.enconding = "utf-8"
    tline = r.text.split("\n")
    for l in tline:
        l = l.strip()
        if len(l) < 1:
            continue
        if l.find(":") < 0:
            continue
        end = l.find("<br")
        if end < 0:
            continue
        l = l[0:end]
        ud = str(int(time.time() * 1000))
        ipm = models.TIpProxy(update_time=ud)
        ipm.src_url = url
        ipm.host = l
        ipm.protocol = "https"
        ipm.proxy_type = 2
        ippool.pushNoCheckIp(ipm)
    # print(ipm)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")

#每分钟从数据库中查询最后可用的200条放入待检测列表
@sched.scheduled_job('interval', seconds=60)
def mydb_query():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "从数据库中获取有效的ip开始-----")
    iplist = models.TIpProxy.objects.order_by("-check_time").all()[:200]
    for ipm in iplist:
        ippool.pushNoCheckIp(ipm)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "从数据库中获取有效的ip结束-----",len(iplist))

def getproxyType(s):
    if len(s) < 1:
        return 0
    if s.find("透明") != -1:
        return 0
    if s.find("高匿") != -1:
        return 2
    if s.find("匿名") != -1:
        return 1
    if s.find("欺诈") != -1:
        return 3
    return 0


#检查IP是否有效的方法，如果有效，则存储到数据库中，并且放入有效ip池中
def checkIp():
    ipm = ippool.popNoCheckIp()
    if ipm is None:
        return
    ret = ipcommon.checkIpCon(ipm)
    if ret:
        ret = ipcommon.checkIpProxy(ipm)
        if ret:
            print("checkIp:" + ipm.host)
            ipm.check_time = int(time.time())
            ipm.save()
            ippool.pushCheckIp(ipm)


#每分钟检测相关的ip是否有效，如果有效，则放入到可用ip池中
@sched.scheduled_job('interval', seconds=30)
def checkIp_job():
    print("checkIp_job:开始" )
    tpool = MyThreadPool.MyThreadPool(10)
    #死循环一直进行检查
    for i in range(300):
        tpool.callInThread(checkIp)

#ip66_query()
if __name__ == '__main__':
    print("sched.start()")
    sched.start()


