# -*- coding: utf-8 -*-
"""
采用原始的mysql对淘宝相关的model进行操作封装
主要针对性能有问题的操作，比如插入，更新等操作进行封装
"""
from mysite.libs import mysqlclient
from mysite.app.taobao import models

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




if __name__ == '__main__':
    shop = models.TTbShop()
    print(shop.shop_createtime is None)

    pass
