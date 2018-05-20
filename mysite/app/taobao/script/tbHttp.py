# -*- coding: utf-8 -*-
import os
import threading
import time
from mysite.libs import myredis
from mysite.libs import stringExt
from mysite.app.taobao import models
from mysite.app.taobao import tbpool
import django
import json
import urllib

from mysite.libs import BaseHttpGet

#所有淘宝的httpget请求处理定义在这里

# 淘宝的商店搜索
# https://shopsearch.taobao.com/search?app=shopsearch&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180405&ie=utf8&loc=%E8%8C%82%E5%90%8D&s=540
class TBShopSearchCrawer(BaseHttpGet.BaseHttpGet):
    url = None
    name = "TBShopSearchCrawer"
    q = None  # 搜索关键字
    city = None  # 搜索城市
    pageno = 1  # 分页数

    # 执行数据爬取前先设置headers
    def before(self):
        isg = tbpool.popISG()
        tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
            'cookie': 'isg={}'.format(isg)
        }
        now = time.strftime("%Y%m%d", time.localtime())

        q = urllib.parse.urlencode({'q':self.q,'loc':self.city})
        turl = "https://shopsearch.taobao.com/search?app=shopsearch&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{0}&ie=utf8&s={1}&{2}"
        self.url = turl.format(now,  self.pageno,q)
        return True

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            rettext = response.text
            # 成功的话，必然包含下面的字符串
            if rettext.find("g_page_config =") == -1:
                return False
            g_pagestr = stringExt.extractLine(rettext, "g_page_config", "pageName")
            if g_pagestr is None:
                return False
            g_pagestr = stringExt.ExtStr(g_pagestr, "g_page_config = ")
            g_pagestr = g_pagestr[:len(g_pagestr)-1]
            # 如果没有shopItems，则抓取结束了
            if g_pagestr.find("shopItems") == -1:
                r.set("TB:ShopSearch:" + self.q + "," + self.city, None, ex=60 * 60 * 6)
                return True
            page = json.loads(g_pagestr)
            items = page["mods"]["shoplist"]["data"]["shopItems"]
            for item in items:
                shop = models.TTbShop()
                shopurl = item["shopUrl"]
                shop.shopid = int(shopurl[shopurl.find("shop") + 4:shopurl.find(".taobao")])
                shop.mainpage = shopurl
                shop.uid = int(item["uid"])
                shop.nick = item["nick"]
                shop.user_rate_url = item['userRateUrl']
                shop.title = item['title']
                shop.shop_score = int(item['totalsold'])
                shop.prod_count = int(item['procnt'])
                shop.shop_area = item['provcity']
                if item["isTmall"] is True:
                    shop.shop_type = "TM"
                else:
                    shop.shop_type = "TB"

                #如果已经存在，则不处理，否则存储
                if tbpool.existKey(shop.shopid):
                    continue
                else:
                    shop.save()

                #执行完，把一下页放入待执行列表
                if self.pageno < 100:
                    self.pageno = self.pageno+1
                    BaseHttpGet.pushHttpGet(self)
        except Exception as e:
            print("TBShopSearchCrawer数据解析出错:",e)

        return True
        pass


# 测试类
class TestHttpGet(BaseHttpGet.BaseHttpGet):
    url = "http://www.baidu.com/"

    def before(self):
        return False

    def parse(self, response):
        print(response.text)
        return True



if __name__ == '__main__':
    print(urllib.parse.urlencode({"q":"吃"}))
    test = TBShopSearchCrawer()
    test.city = "广州"
    test.q = "吃"

    test.run()

    pass
