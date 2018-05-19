# -*- coding: utf-8 -*-
import os
import threading
import time
from mysite.libs import myredis
from mysite.libs import stringExt
import django
import json

from mysite.libs import BaseHttpGet


# 淘宝的商店搜索
# https://shopsearch.taobao.com/search?app=shopsearch&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180405&ie=utf8&loc=%E8%8C%82%E5%90%8D&s=540
class TBShopSearchCrawer(BaseHttpGet):
    name = "TBShopSearchCrawer"
    loc = None
    city = None
    # 执行数据爬取前先设置headers
    def before(self):
        r = myredis.getRedis()
        isg = r.lpop("TB:isg")
        isg = isg.decode()
        r.rpush("TB:isg", isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
            'cookie': 'isg={}'.format(isg)
        }
        #如果已经结束了，则不抓了
        if r.exists("TB:ShopSearch:"+loc+city):
            return False
        return True

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        rettext = response.text
        #成功的话，必然包含下面的字符串
        if rettext.find("g_page_config =")==-1:
            return False
        g_pagestr = stringExt.extractLine(rettext,"g_page_config","pageName")
        if g_pagestr is None:
            return False
        g_pagestr = stringExt.ExtStr(g_pagestr,"g_page_config = ")
        # 如果没有shopItems，则抓取结束了
        if g_pagestr.find("shopItems")==-1:
            r.set("TB:ShopSearch:" + loc + city)
            return True
        page = json.loads(g_pagestr)

        return True
        pass


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
    django.setup()  # 执行
    # 这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    from mysite.app.taobao import models

    shop = tbshop()
    prod = models.TTbShopProd()
    # prods = prod.objects.all()[1:10000]
    for p in range(1, 2000000):
        shop.doAction("567492771957")
        shop.doAction("565923458401")
