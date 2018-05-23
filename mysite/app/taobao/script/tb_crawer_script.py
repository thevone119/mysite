# -*- coding: utf-8 -*-
#淘宝数据处理的定时脚本

import os
import threading
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from mysite.libs import myredis
from mysite.app.taobao import models
from mysite.app.taobao import tbpool
import django
import json
import urllib
from mysite.libs import MyThreadPool
import threadpool

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
    count=0
    for city in cityl:
        for cat in catl:
            tshop = tbHttp.TBShopSearchCrawer()
            tshop.pageno=1
            tshop.q=cat
            tshop.city=city
            tshop.id="shop_search"+city+","+cat
            BaseHttpGet.pushHttpGet(tshop)
            count =count +1
    pass

    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"init_shop_search 结束----",count)


http_lasttime = None
@sched.scheduled_job('interval',id="do_http_job", seconds=60)
def do_http_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"do_http_job 开始----")
    job = sched.get_job(job_id="do_http_job")
    next = int(job.next_run_time.strftime('%Y%m%d%H%M%S'))

    tpool = MyThreadPool.MyThreadPool(40)
    for i in range(10000):
        now = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if next - now < 3:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), i , "do_http_job 结束--------------------------------------------------------")
            return
        tpool.callInThread(do_http)
    pass
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_http_job 提前结束----")

def do_http(i=None):
    http = BaseHttpGet.popHttpGet(tbHttp.TBShopSearchCrawer.__name__)
    if http is None:
        return
    if http.run():
        pass
    else:
        BaseHttpGet.pushHttpGet(http)
        pass


def do_update_shop_create_time():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_update_shop_create_time 开始----")
    count = BaseHttpGet.getHttpGetPoolCount(tbHttp.TBShopCreateTimeCrawer())
    if count>0:
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_update_shop_create_time 还有部分数据未处理完",count)
        return
    list = models.TTbShop.objects.filter(shop_createtime=None)[0:5000]

    for shop in list:
        http = tbHttp.TBShopCreateTimeCrawer()
        http.shopid = shop.shopid
        BaseHttpGet.pushHttpGet(http)
    pass
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_update_shop_create_time 结束----")

if __name__ == '__main__':
    #init_shop_search()
    #do_http()
    sched.start()
    #do_http()
    pass
