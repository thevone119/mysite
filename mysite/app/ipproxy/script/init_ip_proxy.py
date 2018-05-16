# -*- coding: utf-8 -*-
# 把所有代理IP信息进行抓取，然后存储到数据库中，每5分钟进行一次抓取
import os
import json
import datetime
import django
import requests
from bs4 import BeautifulSoup
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
django.setup()  # 执行
# 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
from mysite.app.ipproxy import models


# 抓取西刺代理的数据每5分钟执行一次
# http://www.xicidaili.com/nn/27
@sched.scheduled_job('interval', minutes=5)
def xici_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    for i in range(1, 20):
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
            idx = 0
            for l in tline:
                l = l.strip()
                if len(l) < 1:
                    continue
                if idx == 0:
                    ipm.ip = l
                if idx == 1:
                    ipm.prot = int(l)
                    pass
                if idx == 2:
                    ipm.loc = l
                if idx == 3:
                    ipm.proxy_type = getproxyType(l)
                if idx == 4:
                    ipm.protocol = l
                idx = idx + 1
            ipm.save()
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")
    pass


# 抓取快代理数据，5分钟一次
# https://www.kuaidaili.com/free/inha/2/
@sched.scheduled_job('interval', minutes=5)
def kuaidaili_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    for i in range(1, 30):
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
            idx = 0
            for l in tline:
                l = l.strip()
                if len(l) < 1:
                    continue
                if idx == 0:
                    ipm.ip = l
                if idx == 1:
                    ipm.prot = int(l)
                    pass
                if idx == 4:
                    ipm.loc = l
                if idx == 2:
                    ipm.proxy_type = getproxyType(l)
                if idx == 3:
                    ipm.protocol = l
                idx = idx + 1
            ipm.save()
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
    #url = "http://www.data5u.com/free/gngn/index.shtml"
    print(time.strftime("%d %H:%M:%S",time.localtime(time.time())),"抓取代理网站（",url,")开始-----")
    r = requests.get(url, headers=headers)
    r.enconding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.find_all("ul",attrs={'class':['l2']})
    for tr in trs[1:]:
        txt = tr.text
        if txt.find("http") < 0:
            continue
        tline = txt.split("\n")
        ud = str(int(time.time() * 1000))
        ipm = models.TIpProxy(update_time=ud)
        idx = 0

        for l in tline:
            l = l.strip()

            if len(l) < 1:
                continue
            if idx == 0:
                ipm.ip = l
            if idx == 1:
                ipm.prot = int(l)
                pass
            if idx == 4:
                ipm.loc = l
            if idx == 2:
                ipm.proxy_type = getproxyType(l)
            if idx == 3:
                ipm.protocol = l
            idx = idx + 1
        #print(ipm)
        ipm.save()
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
        ipm.ip = lj['ip']
        ipm.prot = lj['port']
        ipm.protocol = "HTTPS"
        ipm.proxy_type = 2
        ipm.loc = lj['addr']
        ipm.save()
    pass
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")


# 抓取66ip代理数据，5分钟一次
# http://www.66ip.cn/
@sched.scheduled_job('interval', seconds=30)
def ip66_query():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    url = "http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip"
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")开始-----")
    r = requests.get(url, headers=headers)
    r.enconding = "utf-8"
    tline = r.text.split("\n")
    for l in tline:
        l = l.strip()
        if len(l) < 1:
            continue
        if l.find(":")<0:
            continue
        end = l.find("<br")
        if end < 0:
            continue

        l = l[0:end]
        ipp = l.split(":")
        ud = str(int(time.time() * 1000))
        ipm = models.TIpProxy(update_time=ud)
        ipm.ip = ipp[0]
        ipm.prot = int(ipp[1])
        ipm.protocol="https"
        ipm.proxy_type=2
        ipm.save()
    # print(ipm)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取代理网站(", url, ")结束-----")


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




#ip66_query()

sched.start()
