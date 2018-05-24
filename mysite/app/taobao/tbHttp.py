# -*- coding: utf-8 -*-
import os
import threading
import time
from mysite.libs import myredis
from mysite.libs import stringExt
from mysite.app.taobao import models
from mysite.app.taobao import tbpool
from mysite.app.taobao import tbcategory
import django
import json
import urllib

from mysite.libs import BaseHttpGet
from mysite.libs import file_int

# 所有淘宝的httpget请求处理定义在这里

CRA_COUNT = 0
# 全局锁
L_CAT = threading.Lock()



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
        global CRA_COUNT
        L_CAT.acquire()
        CRA_COUNT = CRA_COUNT + 1
        L_CAT.release()
        isg = tbpool.popISG()

        tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
            'cookie': 'isg={}'.format(isg)
        }
        now = time.strftime("%Y%m%d", time.localtime())

        q = urllib.parse.urlencode({'q': self.q, 'loc': self.city})
        turl = "https://shopsearch.taobao.com/search?app=shopsearch&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{0}&ie=utf8&s={1}&{2}"
        self.url = turl.format(now, self.pageno, q)
        return True

    def nextQuery(self):
        n_q = tbcategory.getNextQueryKey(self.q)
        if n_q is not None:
            self.q = n_q
            self.id = None  # id必须设置为空，否则无放入到运行队列里
            self.pageno = 1
            BaseHttpGet.pushHttpGet(self)
        return

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            rettext = response.text
            # 成功的话，必然包含下面的字符串
            if rettext.find("g_page_config =") == -1:
                if CRA_COUNT % 50 == 0:
                    print("数据抓取错误：", rettext, CRA_COUNT)
                return False

            g_pagestr = stringExt.StringExt(rettext).extractLine( "g_page_config", "pageName").ExtStr("g_page_config = ").str()
            if g_pagestr is None:
                return False
            g_pagestr = g_pagestr[:len(g_pagestr) - 1]
            # 如果没有shopItems，则抓取结束了
            if g_pagestr.find("shopItems") == -1:
                self.nextQuery()
                return True
            page = json.loads(g_pagestr)
            items = page["mods"]["shoplist"]["data"]["shopItems"]
            itemcount = 0
            sesscount = 0
            for item in items:
                itemcount = itemcount + 1
                shopurl = item["shopUrl"]
                shopid = self.paseInt(shopurl[shopurl.find("shop") + 4:shopurl.find(".taobao")])
                #如果在缓存中存在，则直接跳过
                if tbpool.ShopIdExist(shopid):
                    continue
                #查找数据库中是否存在，如果存在，则直接跳过，如果不存在，则新建一个,避免了把旧的数据替换掉的问题
                shop = models.TTbShop.objects.filter(shopid=shopid).first()
                if shop is None:
                    sesscount = sesscount + 1
                    shop = models.TTbShop()
                    shop.shopid = shopid
                else:
                    continue
                shop.mainpage = shopurl
                shop.uid = self.paseInt(item["uid"])
                shop.nick = item["nick"]
                shop.user_rate_url = item['userRateUrl']
                shop.title = item['title']
                # shop.shop_score = self.paseInt(item['totalsold'])
                shop.prod_count = self.paseInt(item['procnt'])
                shop.shop_area = item['provcity']
                if item["isTmall"] is True:
                    shop.shop_type = "TM"
                else:
                    shop.shop_type = "TB"
                shop.save()
            pass
            # 如果整页都没有一条新的的，则直接跳过10页
            if sesscount == 0:
                self.pageno = self.pageno+10
            # 每20条输出一条
            if CRA_COUNT % 50 == 0:
                print("数据抓取结束", self.city, self.q, self.pageno, CRA_COUNT, itemcount)
            # 执行完，把一下页放入待执行列表,如果超过100页，则把下一个关键字放入
            if self.pageno < 100:
                self.pageno = self.pageno + 1
                self.id = None  # id必须设置为空，否则无放入到运行队列里
                BaseHttpGet.pushHttpGet(self)
            else:
                self.nextQuery()
        except Exception as e:
            print("TBShopSearchCrawer数据解析出错:", e)
            return False
        return True
        pass


#获取淘宝的店铺的创建时间
class TBShopCreateTimeCrawer(BaseHttpGet.BaseHttpGet):
    shopid=None
    isProxy = True
    # 执行数据爬取前先设置headers
    def before(self):
        self.isProxy = True
        global CRA_COUNT
        L_CAT.acquire()
        CRA_COUNT = CRA_COUNT + 1
        L_CAT.release()
        isg = tbpool.popISG()
        tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'
        }
        now = time.strftime("%Y%m%d", time.localtime())
        rd = time.time()
        turl = "https://shop.taobao.com/getShopInfo.htm?shopId={0}&staobaoz_{1}&rd={2}"
        self.url = turl.format(self.shopid,now, rd)
        return True

    def parse(self, response):
        try:
            shopCreatetime = stringExt.StringExt(response.text).ExtStr("starts\":\"","\"}").str()
            if shopCreatetime == None:
                print("获取时间失败", response.text)
                return False
            #更新数据
            shop = models.TTbShop.objects.get(shopid=self.shopid)
            shop.shop_createtime = shopCreatetime
            shop.save()
            print("获取时间成功", self.shopid)
        except Exception as e:
            print("TBShopCreateTimeCrawer数据解析出错:", e)
            return False
        return True


class TBProdSearchCrawer(BaseHttpGet.BaseHttpGet):
    url = None
    name = "TBProdSearchCrawer"
    q = None  # 搜索关键字
    city = None  # 搜索城市
    pageno = 1  # 分页数

    # 执行数据爬取前先设置headers
    def before(self):
        global CRA_COUNT
        L_CAT.acquire()
        CRA_COUNT = CRA_COUNT + 1
        L_CAT.release()
        isg = tbpool.popISG()
        tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
            'cookie': 'isg={}'.format(isg)
        }
        now = time.strftime("%Y%m%d", time.localtime())

        q = urllib.parse.urlencode({'q': self.q, 'loc': self.city})
        turl = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_${0}&stats_click=search_radio_all%3A1&js=1&imgfile=&_input_charset=utf-8&s=${1}&{2}"
        pageSize = 44
        s = self.pageno * pageSize - pageSize
        self.url = turl.format(now, s, q)
        return True

    def nextQuery(self):
        n_q = tbcategory.getNextQueryKey(self.q)
        if n_q is not None:
            self.q = n_q
            self.id = None  # id必须设置为空，否则无放入到运行队列里
            self.pageno = 1
            BaseHttpGet.pushHttpGet(self)
        return

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            rettext = response.text
            # 成功的话，必然包含下面的字符串
            if rettext.find("g_page_config =") == -1:
                if CRA_COUNT % 50 == 0:
                    print("数据抓取错误：", rettext, CRA_COUNT)
                return False
            st = stringExt.StringExt(rettext)
            g_pagestr = st.extractLine( "g_page_config", "pageName").ExtStr("g_page_config = ").str()

            if g_pagestr is None:
                return False
            g_pagestr = g_pagestr[:len(g_pagestr) - 1]
            # 如果没有auctions，则抓取结束了
            if g_pagestr.find("auctions") == -1:
                self.nextQuery()
                return True
            page = json.loads(g_pagestr)
            items = page["mods"]["itemlist"]["data"]["auctions"]
            itemcount = 0
            sesscount = 0
            for item in items:
                itemcount = itemcount + 1
                product_id = item["nid"]
                product_id = self.paseInt(product_id)
                if product_id is None:
                    continue

                view_sales = stringExt.StringExt(item["view_sales"]).ExtStr("", "人").int()
                if view_sales is not None:
                    if view_sales==0:
                        continue
                #如果在缓存中存在，则直接跳过
                if tbpool.prodIdExist(product_id):
                    continue
                #查找数据库中是否存在，如果存在，则直接跳过，如果不存在，则新建一个,避免了把旧的数据替换掉的问题
                prod = models.TTbShopProd.objects.filter(product_id=product_id).first()
                if prod is None:
                    prod = models.TTbShopProd()
                    prod.product_id = product_id
                else:
                    continue
                prod.loc = item["item_loc"]
                prod.name = item["raw_title"]
                prod.uid = item["user_id"]
                prod.view_sales = view_sales

                prod.shop_price = self.paseInt(item["view_price"] *100)
                prod.save()
                sesscount = sesscount + 1

            pass
            # 如果整页都没有一条新的的，则直接跳过10页
            if sesscount == 0:
                self.pageno = self.pageno+10
            # 每20条输出一条
            if CRA_COUNT % 50 == 0:
                print("数据抓取结束", self.city, self.q, self.pageno, CRA_COUNT, itemcount)
            # 执行完，把一下页放入待执行列表,如果超过100页，则把下一个关键字放入
            if self.pageno < 100:
                self.pageno = self.pageno + 1
                self.id = None  # id必须设置为空，否则无放入到运行队列里
                BaseHttpGet.pushHttpGet(self)
            else:
                self.nextQuery()
        except Exception as e:
            print("TBProdSearchCrawer数据解析出错:", e)
            return False
        return True
        pass


#淘宝商家主页
class TBShopMainCrawer(BaseHttpGet.BaseHttpGet):
    shopid=None
    uid=None
    isProxy = False
    encoding = 'GBK'
    # 执行数据爬取前先设置headers
    def before(self):
        global CRA_COUNT
        L_CAT.acquire()
        CRA_COUNT = CRA_COUNT + 1
        L_CAT.release()
        #isg = tbpool.popISG()
        #tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'
        }
        now = time.strftime("%Y%m%d", time.localtime())
        rd = time.time()
        if self.uid is not None:
            turl = "https://store.taobao.com/shop/view_shop.htm?user_number_id={0}"
            self.url = turl.format(self.uid)

        if self.shopid is not None:
            turl = "https://shop{0}.taobao.com"
            self.url = turl.format(self.shopid)
        return True

    def parse(self, response):
        try:
            html = response.text
            if html.find("window.shop_config")<1:
                print("获取商家主页数据失败", html)
                return False

            st = stringExt.StringExt(html)
            shopname_l = st.extractLine("shop-name","<a class=")
            shopname = shopname_l.ExtStr("<span>","</span>").str()
            shopurl = shopname_l.ExtStr( "href=\"", "\"").str()
            if shopname is None:
                shopname_l = st.extractLine("shop-name-title","<span")
                shopname = shopname_l.ExtStr("\">","</span>").str()

            shop_config = st.ExtStr("window.shop_config =","};").str()
            jobj = json.loads(shop_config+"}")
            userId = jobj["userId"]
            shopId = jobj["shopId"]
            user_nick = urllib.parse.unquote(jobj["user_nick"])
            userRateUrlstr = st.extractLine("<a ","//rate.taobao.com/").ExtStr("href=\"","\"").str()
            shopType = "TB"
            if st.indexCount("tmall.com") > 5:
                shopType = "TM"
            #描述分数
            itemScore = st.extractLine("dsr-num red","</span>",html.find("描述")).ExtStr("red\">","</span>").float()
            # 服务分数
            serviceScore = st.extractLine("dsr-num red", "</span>", html.find("服务")).ExtStr("red\">", "</span>").float()
            # 物流分数
            deliveryScore = st.extractLine("dsr-num red", "</span>", html.find("物流")).ExtStr("red\">", "</span>").float()

            # 查找数据库中是否存在，如果存在，则直接跳过，如果不存在，则新建一个,避免了把旧的数据替换掉的问题
            shop = models.TTbShop.objects.filter(shopid=shopId).first()
            if shop is None:
                shop = models.TTbShop()
                shop.shopid = shopId
            if userId is not None:
                shop.uid=userId
            if shopurl is not None:
                shop.mainpage = shopurl
            if user_nick is not None:
                shop.nick = user_nick
            if userRateUrlstr is not None:
                shop.user_rate_url = userRateUrlstr
            if shopType is not None:
                shop.shop_type = shopType
            if shopname is not None:
                shop.title = shopname
            if itemScore is not None:
                shop.item_score = itemScore
            if serviceScore is not None:
                shop.service_score = serviceScore
            if deliveryScore is not None:
                shop.delivery_score = deliveryScore
            shop.save()

            print("获取商家主页数据成功", self.shopid)
        except Exception as e:
            print("TBShopMainCrawer数据解析出错:", e)
            return False
        return True

#淘宝卖家主页
class TBUserRateCrawer(BaseHttpGet.BaseHttpGet):
    shopid=None
    isProxy = False
    encoding = 'utf-8'
    # 执行数据爬取前先设置headers
    def before(self):
        global CRA_COUNT
        L_CAT.acquire()
        CRA_COUNT = CRA_COUNT + 1
        L_CAT.release()
        isg = tbpool.popISG()

        tbpool.pushISG(isg)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3',
            'cookie': 'thw=cn; miid=1714981155805935700; l=AuLiW6Rw6YNZPxWqb9bnun/GsmZEIeZN; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; cna=OCTpEf5FVnICAbcSF1gbeE0t; enc=RuTtWZsEqNoVCw9IiMgDmkTxqomSox1fA3oNqqL3FbJduKivwZ4t4dgyoVikI5PdZxbNF4IlNapOCWJeQ4eA6w%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; tg=4; __guid=98467100.3035049717173234700.1526318952720.6155; UM_distinctid=16381b67eaaa4-0f4c5b9b527742-6b1b1279-1fa400-16381b67eab3d1; t=bff7b50a0ccb05c2971af4a6d23790de; cookie2=4c61466f8ac6a279657d99cbbe18dba5; _m_h5_tk=9fff7c177859177a1c5a1580e2282feb_1527053309996; _m_h5_tk_enc=2bcf7a113c1939598fc9d9f84d913e8a; ali_ab=119.135.76.7.1527050969284.8; _tb_token_=33fe57e37d43e; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=0_0; v=0; monitor_count=8; isg=BJaWZzr00WT0fue32R0slRmY50xYn9sZ9enpFAD_uHkUwzZdaMcqgfy7X18v69KJ',
            'referer':'https://ss163.taobao.com/shop/view_shop.htm?spm=a219r.lm874.14.8.5fec6dbc0luSwy&user_number_id=42314291',
        }
        return True

    def parse(self, response):
        try:
            html = response.text
            if html.find("卖家信用")<1:
                print("获取淘宝卖家主页数据失败", html)
                return False
            st = stringExt.StringExt(html)
            shopArea = st.extractLine("<li>所在地区").ExtStr("所在地区：","</li>").str()
            mainCname = st.extractLine("<span id=\"chart-name\" class=\"data\">").ExtStr("class=\"data\">","</span>").str()
            if mainCname is None:
                mainCname = st.extractLine("<li>当前主营").ExtStr("target=\"_blank\">","</a>").str()

            # 近半年评分人数 // 共 < span > 5056965 < / span > 人
            commentCount = st.extractLine("共<span>","</span>人").ExtStr("<span>","</span>").int()

            itemScore= st.extractLine("<em title","class=\"count\"",beg=html.find("宝贝与描述相符")).ExtStr("class=\"count\">","</em>").float()
            serviceScore=st.extractLine("<em title","class=\"count\"",beg=html.find("卖家的服务态度")).ExtStr("class=\"count\">","</em>").float()
            deliveryScore=st.extractLine("<em title","class=\"count\"",beg=html.find("物流服务的质量")).ExtStr("class=\"count\">","</em>").float()

            sellerCredit = st.extractLine("<span id=\"chart-num\" class=\"data\">").ExtStr("class=\"data\">","</span>").int()
            if sellerCredit is None:
                sellerCredit = st.extractLine("<div class=\"list\">卖家信用").ExtStr("卖家信用：").int()

            # 查找数据库中是否存在，如果存在，则直接跳过，如果不存在，则新建一个,避免了把旧的数据替换掉的问题
            shop = models.TTbShop.objects.filter(shopid=self.shopid).first()
            if shop is None:
                shop = models.TTbShop()
                shop.shopid = self.shopid
            if shopArea is not None:
                shop.shop_area = shopArea
            if mainCname is not None:
                shop.main_cname = mainCname
            if commentCount is not None:
                shop.comment_count = commentCount
            if sellerCredit is not None:
                shop.seller_credit = sellerCredit
            if itemScore is not None:
                shop.item_score = itemScore
            if serviceScore is not None:
                shop.service_score = serviceScore
            if deliveryScore is not None:
                shop.delivery_score = deliveryScore
            shop.save()

            print("获取淘宝卖家主页数据成功", self.shopid)
        except Exception as e:
            print("TBUserRateCrawer数据解析出错:", e)
            return False
        return True

# 测试类
class TestHttpGet(BaseHttpGet.BaseHttpGet):
    url = "http://www.baidu.com/"

    def before(self):
        return False

    def parse(self, response):
        print(response.text)
        return True


if __name__ == '__main__':

    test = TBUserRateCrawer()
    test.shopid = 33757521
    test.url = "https://rate.taobao.com/user-rate-UMmIGvFQyOFHT.htm?spm=a1z10.1-c-s.0.0.20c375c0IN5YFU"
    test.run()


    #test.run()

    pass
