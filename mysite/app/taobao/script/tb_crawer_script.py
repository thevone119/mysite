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

def do_http(clasName=None):
    http = BaseHttpGet.popHttpGet(clasName)
    if http is None:
        return
    if http.run():
        pass
    else:
        BaseHttpGet.pushHttpGet(http)
        pass


#@sched.scheduled_job('interval',id="shop_search_job", seconds=60)
def shop_search_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"shop_search_job 开始----")
    job = sched.get_job(job_id="shop_search_job")
    next = int(job.next_run_time.strftime('%Y%m%d%H%M%S'))
    clasName = tbHttp.TBShopSearchCrawer.__name__
    count = BaseHttpGet.getHttpGetPoolCount(clasName)
    # 如果队列中的元素为空，则加入一批到队列中(放在提前结束的逻辑去)
    if count == 0:
        pass
    #开启40个线程进行处理
    tpool = MyThreadPool.MyThreadPool(20)
    for i in range(10000):
        now = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if next - now < 3:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), i , "shop_search_job 结束--------------------------------------------------------")
            return
        tpool.callInThread(do_http,clasName)
    pass
    #如果要提前结束，则加入一批待处理
    cityl = chinaCity.listAllCity()
    cat = tbcategory.getFristQueryKey()
    for city in cityl:
        tshop = tbHttp.TBShopSearchCrawer()
        tshop.pageno = 1
        tshop.q = cat
        tshop.city = city
        # tshop.id = "shop_search," + cat + city
        BaseHttpGet.pushHttpGet(tshop)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "shop_search_job 提前结束----")


@sched.scheduled_job('interval',id="prod_search_job", seconds=60)
def prod_search_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"prod_search_job 开始----")
    job = sched.get_job(job_id="prod_search_job")
    next = int(job.next_run_time.strftime('%Y%m%d%H%M%S'))
    clasName = tbHttp.TBProdSearchCrawer.__name__
    count = BaseHttpGet.getHttpGetPoolCount(clasName)
    # 如果队列中的元素为空，则加入一批到队列中
    if count < 10:
        pass
    #开启40个线程进行处理
    tpool = MyThreadPool.MyThreadPool(40)
    for i in range(10000):
        now = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if next - now < 3:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), i , "prod_search_job 结束--------------------------------------------------------")
            return
        tpool.callInThread(do_http,clasName)
    pass
    #如果要提前结束，则放入一批新的查询

    cityl = chinaCity.listAllCity()
    cat = tbcategory.getFristQueryKey()
    #先放入一个没有城市划分的
    prod = tbHttp.TBProdSearchCrawer()
    prod.pageno = 1
    prod.q = cat
    BaseHttpGet.pushHttpGet(prod)
    for city in cityl:
        prod = tbHttp.TBProdSearchCrawer()
        prod.pageno = 1
        prod.q = cat
        prod.city = city
        BaseHttpGet.pushHttpGet(prod)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "prod_search_job 提前结束----")


#@sched.scheduled_job('interval',id="update_shop_create_time_job", seconds=60)
def update_shop_create_time_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_update_shop_create_time 开始----")
    job = sched.get_job(job_id="update_shop_create_time_job")
    next = int(job.next_run_time.strftime('%Y%m%d%H%M%S'))
    clasName = tbHttp.TBShopCreateTimeCrawer.__name__
    count = BaseHttpGet.getHttpGetPoolCount(clasName)

    #如果队列中的元素为空，则加入一批到队列中
    if count==0:
        list = models.TTbShop.objects.filter(shop_createtime=None)[0:5000]
        for shop in list:
            http = tbHttp.TBShopCreateTimeCrawer()
            http.shopid = shop.shopid
            http.isProxy = True
            BaseHttpGet.pushHttpGet(http)
        pass
    #开启线程进行处理
    tpool = MyThreadPool.MyThreadPool(5)
    for i in range(10000):
        now = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if next - now < 10:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), i,
                  "update_shop_create_time_job 结束--------------------------------------------------------")
            return
        tpool.callInThread(do_http,clasName)
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "do_update_shop_create_time 提前结束----")
    pass


if __name__ == '__main__':
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "sched.start()")
    sched.start()
    pass
