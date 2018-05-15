# -*- coding: utf-8 -*-
import os
# 导入Django
import django


def doAction(self, id):
    pass

    return




if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话

    django.setup()  # 执行
    # 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    from mysite.app.ipproxy import models

