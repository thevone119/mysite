# -*- coding: utf-8 -*-
#获取淘宝的常用字

import time


from mysite.libs import BaseHttpGet
from mysite.libs import chinaCity
from mysite.app.taobao import tbcategory
from mysite.app.taobao import tbHttp

def init_shop_search():
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"init_shop_search 开始----")
    cityl = chinaCity.listAllCity()
    catl = tbcategory.listAllCat()
    count=0
    for city in cityl:
        for cat in catl:
            tshop = tbHttp.TBShopSearchCrawer()
            tshop.pageno=1
            tshop.q=cat
            tshop.city=city
            tshop.id="shop_search,"+cat+city
            BaseHttpGet.pushHttpGet(tshop)
            count =count +1
        pass

    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())),"init_shop_search 结束----",count)

if __name__ == '__main__':
    init_shop_search()