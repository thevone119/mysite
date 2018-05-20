# -*- coding: utf-8 -*-
import os
import threading
import time
import random
import django


# 淘宝的商店搜索页面
class tbshopSearch(object):
    itemdriver = None
    count = 0
    city = '广州'



# 全局锁
mutex = threading.Lock()
cBaseUrl = "https://shopsearch.taobao.com/search?app=shopsearch&q=${q}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_${now}&ie=utf8&loc=${loc}&s=${s}";

if __name__ == '__main__':
    pass
