# -*- coding: utf-8 -*-
"""
采用原始的mysql对淘宝相关的model进行操作封装
主要针对性能有问题的操作，比如插入，更新等操作进行封装
"""
from mysite.libs import mysqlclient
from mysite.app.taobao import models
import jieba
from mysite.app.taobao import models
import random


def ShopSaveOrUpdate(shop):
    _shop = models.TTbShop.objects.get(shopid=shop.shopid)
    if _shop is None:
        shop.save()
    else:
        if shop.shop_createtime is not None:
            _shop.shop_createtime = shop.shop_createtime
        if shop.shop_area is not None:
            _shop.shop_area = shop.shop_area
        if shop.shop_score is not None:
            _shop.shop_score = shop.shop_score
        if shop.item_score is not None:
            _shop.item_score = shop.item_score
    pass


def random_shop_name():
    """
    随机抽取100条记录，获取分词，获取排名前1000的分词结果
    1.只要2-5位的分词结果，不要单个字的
    """
    dict = {}
    start = random.randint(0,10000)
    start=start*100
    list = models.TTbShop.objects.all()[start:start+100]
    for shop in list:
        if shop.title is None:
            continue
        cut = jieba.cut(shop.title)
        for c in cut:
            if c in dict:
                dict[c]=dict[c]+1
            else:
                dict[c] = 1
    slist = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    count=0
    rlist=[]
    for l in slist:
        count = count+1
        if count>1000:
            break
        rlist.append(l[0])
    return rlist

def random_prod_name():
    """
    随机抽取100条记录，获取分词，获取排名前1000的分词结果
    1.只要2-5位的分词结果，不要单个字的
    """
    dict = {}
    start = random.randint(0,10000)
    start=start*100
    list = models.TTbShopProd.objects.all()[start:start+100]
    for prod in list:
        if prod.name is None:
            continue
        cut = jieba.cut(prod.name)
        for c in cut:

            if c in dict:
                dict[c]=dict[c]+1
            else:
                dict[c] = 1
    slist = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    count=0
    rlist=[]
    for l in slist:
        count = count+1
        if count>1000:
            break
        rlist.append(l[0])
    return rlist


if __name__ == '__main__':
    list = random_shop_name()
    print(len(list))
    for k in list:
        print(k)

    pass
