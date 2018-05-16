# -*- coding: utf-8 -*-
#把所有代理IP信息进行抓取，然后存储到数据库中，每5分钟进行一次抓取
import os
import django
import requests
from bs4 import BeautifulSoup
import time
from apscheduler.schedulers.blocking import BlockingScheduler



sched = BlockingScheduler()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
django.setup()  # 执行
# 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
from mysite.app.ipproxy import models

def doAction(self, id):

    pass

    return

def checkProxy():

    pass

#每1分钟执行一次
@sched.scheduled_job('interval', minutes=1)
def my_job2():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    r = requests.get('https://www.baidu.com/', headers=headers)
    r.enconding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.title)








sched.start()
