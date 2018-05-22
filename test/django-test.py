# -*- coding: utf-8 -*-
import os
# 导入Django
import django
from mysite.app.taobao import models
from mysite.libs.MyThreadPool import MyThreadPool


def testThread():
    result = models.TTempObj.objects.filter(obj_key="1").first()
    print(result is None)


if __name__ == '__main__':
    #这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    #test2 = models.TTbShopData.objects.all()
    test1 = models.TTempObj(obj_key='obj_key2',obj_type="obj_type2")
    #test1.save()
    t = MyThreadPool(10)
    for i in range(10):
        t.callInThread(testThread)
    #ORM





