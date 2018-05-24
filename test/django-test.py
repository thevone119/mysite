# -*- coding: utf-8 -*-
import os
# 导入Django
import django
from mysite.app.taobao import models
from mysite.libs.MyThreadPool import MyThreadPool
from mysite.libs import myredis
import time

def testThread():
    result = models.TTempObj.objects.filter(obj_key="1").first()
    print(result is None)


if __name__ == '__main__':
    #这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    #test2 = models.TTbShopData.objects.all()
    #test1 = models.TTempObj(obj_key='obj_key2',obj_type="obj_type2")
    lista = models.TTbShop.objects.all()
    for p in range(100):
        print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"删除1万条数据",p)
        list = lista[p*10000:(p+1)*10000]
        for shop in list:
            myredis.getRedis().delete("TB:EX:"+str(shop.shopid))
    #ORM





