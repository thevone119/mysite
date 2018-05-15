# -*- coding: utf-8 -*-
import os
# 导入Django
import django


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话

    django.setup()  # 执行
    #这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    from mysite.app.taobao import models

    #test2 = models.TTbShopData.objects.all()
    test1 = models.TTempObj(obj_key='obj_key2',obj_type="obj_type2")
    #test1.save()

    #ORM

    result = models.TTempObj.objects.all()
    for a in result:
        print (a.obj_key)



