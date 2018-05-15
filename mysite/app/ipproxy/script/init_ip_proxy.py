# -*- coding: utf-8 -*-
import os
# 导入Django
import django
import requests

def doAction(self, id):

    pass

    return




if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话

    django.setup()  # 执行
    # 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    from mysite.app.ipproxy import models


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    r = requests.get('https://www.baidu.com/',headers=headers)
    r.enconding = "utf-8"
    print(r.text)