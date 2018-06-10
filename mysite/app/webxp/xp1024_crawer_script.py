# -*- coding: utf-8 -*-


import os
import threading
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from mysite.libs import MyThreadPool
from mysite.libs import BaseHttpGet
from mysite.app.webxp import xp1024Http


#网站的跟路径
xp_base_url="http://d2.sku117.info"

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


#@sched.scheduled_job('interval',id="xp1024_search_job", seconds=60)
def xp1024_search_job():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"xp1024_search_job 开始----")
    for i in range(1, 20):
        http=xp1024Http.xp1024_list_crawer()
        http.url=xp_base_url+"/pw/thread.php?fid=5&page=" + str(i)
        http.pub_type="亚洲无码"
        BaseHttpGet.pushHttpGet(http)
    for i in range(1, 20):
        http=xp1024Http.xp1024_list_crawer()
        http.url=xp_base_url+"/pw/thread.php?fid=22&page=" + str(i)
        http.pub_type="日本骑兵"
        BaseHttpGet.pushHttpGet(http)
    for i in range(1, 20):
        http=xp1024Http.xp1024_list_crawer()
        http.url=xp_base_url+"/pw/thread.php?fid=7&page=" + str(i)
        http.pub_type="歐美新片"
        BaseHttpGet.pushHttpGet(http)

    #执行多线程处理
    # 开启5个线程进行处理

    tpool = MyThreadPool.MyThreadPool(5)
    for i in range(10000):
        if BaseHttpGet.getHttpGetPoolCount(xp1024Http.xp1024_list_crawer.__name__)==0:
            break
        tpool.callInThread(do_http, xp1024Http.xp1024_list_crawer.__name__)
    pass

    for i in range(10000):
        if BaseHttpGet.getHttpGetPoolCount(xp1024Http.xp1024_info_crawer.__name__) == 0:
            break
        tpool.callInThread(do_http,  xp1024Http.xp1024_info_crawer.__name__)
    pass
    tpool.wait()

    #执行完数据采集，则执行数据生成，取5天的数据来做数据生成







if __name__ == '__main__':
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "sched.start()")
    #sched.start()
    #update_prod_item_job()
    xp1024_search_job()
    pass
