# -*- coding: utf-8 -*-

import threading
import time
from mysite.app.taobao import tbpool

#淘宝的商店搜索页面

from selenium import webdriver

#全局锁
mutex = threading.Lock()








def initCookie():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2, "permissions.default.stylesheet": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    itemdriver = webdriver.Chrome(chrome_options=chrome_options)
    cBaseUrl = "https://www.taobao.com/?s={}".format(time.time()*1000);
    itemdriver.get(cBaseUrl)


    try:
        for i in range(20):
            c = itemdriver.get_cookie("cookie2")
            if c is None:
                time.sleep(0.1)
            else:
                break
        cookies = itemdriver.get_cookies()
        cook_str = ""
        for c in cookies:
            cook_str = cook_str+c["name"]+"="+c["value"]+"; "

        cook_str=cook_str+"_rd="+str(time.time())

        print(cook_str)
        tbpool.pushNoLoginCookie(cook_str)
        return
    except BaseException:
        pass
    finally:
        itemdriver.close()


if __name__ == '__main__':
    for i in range(1000):
        initCookie()
    pass





