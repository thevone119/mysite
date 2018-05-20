# -*- coding: utf-8 -*-
#淘宝数据处理的定时脚本

import os
import threading
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from mysite.libs import stringExt
from mysite.app.taobao import models
from mysite.app.taobao import tbpool
import django
import json
import urllib
from mysite.libs import MyThreadPool

from mysite.libs import BaseHttpGet
from mysite.libs import chinaCity
from mysite.app.taobao import tbcategory
from mysite.app.taobao import tbHttp


sched = BlockingScheduler()



@sched.scheduled_job('interval', minutes=30)
def init_shop_search_job():
    #init_shop_search()
    pass


def init_shop_search():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"init_shop_search 开始----")
    cityl = chinaCity.listAllCity()
    catl = tbcategory.listAllCat()
    for city in cityl:
        for cat in catl:
            tshop = tbHttp.TBShopSearchCrawer()
            tshop.pageno=1
            tshop.q=cat
            tshop.city=city
            tshop.id="shop_search"+city+","+cat
            BaseHttpGet.pushHttpGet(tshop)
    pass
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"init_shop_search 结束----")


http_lasttime = None
@sched.scheduled_job('interval', seconds=600)
def do_http_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"do_http_job 开始----")
    global http_lasttime
    if http_lasttime is None:
        http_lasttime = datetime.datetime.now()
    tpool = MyThreadPool.MyThreadPool(10)
    while True:
        s = (datetime.datetime.now() - http_lasttime).seconds
        if s > 580:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"do_http_job 结束----")
            return
        http = BaseHttpGet.popHttpGet()
        tpool.callInThread(do_http,http)


def do_http(http=None):
    if http.run():
        pass
    else:
        BaseHttpGet.pushHttpGet(http)
        pass

if __name__ == '__main__':
    init_shop_search()
    sched.start()
    pass
