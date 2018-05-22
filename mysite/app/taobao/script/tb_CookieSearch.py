# -*- coding: utf-8 -*-

import threading
import time
from mysite.app.taobao import tbpool

#淘宝的商店搜索页面

from selenium import webdriver

#全局锁
mutex = threading.Lock()

itemdriver = None


def initWebDriver():
    global itemdriver
    if itemdriver is not None:
        return
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2, "permissions.default.stylesheet": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    itemdriver = webdriver.Chrome(chrome_options=chrome_options)



def closeWebDriver():
    global itemdriver
    itemdriver.close()

def initCookie():
    initWebDriver()
    global itemdriver
    cBaseUrl = "https://www.taobao.com/?s={}".format(time.time()*1000);
    itemdriver.get(cBaseUrl)
    try:
        isg = itemdriver.get_cookie("isg")['value']
        tbpool.pushISG(isg)
        #cookie = itemdriver.execute_script("return document.title")  # js
        #print(cookie)
        return
    except BaseException:
        pass



if __name__ == '__main__':
    for i in range(6000):
        initCookie()
    pass
    closeWebDriver()




