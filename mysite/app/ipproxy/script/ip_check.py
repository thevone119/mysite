# -*- coding: utf-8 -*-
# 对数据库中的代理IP进行定期检测，检测到可用的放入缓存中备用
import os

import django
import time
from mysite.app.ipproxy import ipcommon
from mysite.app.ipproxy import ippool
from mysite.libs import MyThreadPool
from mysite.app.ipproxy import models





def checkIp():
    ipm = ippool.popNoCheckIp()
    ret = ipcommon.checkIpCon(ipm)
    if ~ret:
        return
    print("startip:" + ipm.host)
    ret = ipcommon.checkIpProxy(ipm)
    if ~ret:
        return
    print("checkIp:" + ipm.host)
    ipm.check_time = int(time.time())
    ipm.save()
    ippool.pushCheckIp(ipm)
    return



# 加载有效的ip，匿名的ip到缓存中
def loadActiveIp():
    #开启10个线程对ip进行校验处理,每次校验1000个
    tpool = MyThreadPool.MyThreadPool(8)
    for i in range(1000):
        tpool.callInThread(checkIp)
        #checkIp()



if __name__ == '__main__':
    # 死循环，一直检测ip是否可用
    while True:
        loadActiveIp()
        time.sleep(3)
