# -*- coding: utf-8 -*-
import os
import threading
import time
import random
import django


from selenium import webdriver

#全局锁
mutex = threading.Lock()
#多继承，继承泛滥
class item(object):
    itemdriver = None
    count = 0;
    def initDriver(self):
        if(mutex.acquire()):
            if (self.itemdriver == None):
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.managed_default_content_settings.images": 2, "permissions.default.stylesheet": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                self.itemdriver = webdriver.Chrome(chrome_options=chrome_options)
            mutex.release()

    # 淘宝商品item页面数据抓取,针对不同的商品明细页面进行大数据抓取
    # https://item.taobao.com/item.htm?spm=a219r.lm874.14.21.46a970e411pyHg&id=xxxx


    def doAction(self,id):
        self.initDriver()
        spm = "a"+str(random.randint(1, 99))+"." + str(random.randint(1, 99)) + "." + str(random.randint(1, 99)) + ".46a"+str(random.randint(1, 99))+"e411pyHg"
        url = "https://item.taobao.com/item.htm?id=" + str(id)+"&spm="+spm
        self.itemdriver.get(url)
        #self.itemdriver.maximize_window()  # 窗口最大化，可有可无，看情况
        #获取各种数据
        try:
            close = self.itemdriver.find_element_by_xpath('//*[@id="sufei-dialog-close"]')
            print ("出现关闭按钮")
            close.click()
            return
        except BaseException:
           pass
        else:
            pass

        try:
            sendcity = self.itemdriver.find_element_by_xpath('//*[@id="J_WlAddressInfo"]')
            price = self.itemdriver.find_element_by_xpath('//*[@id="J_StrPrice"]/em[2]')
            shop_price = self.itemdriver.find_element_by_xpath('//*[@id="J_PromoPriceNum"]')
            self.count=self.count+1
            print (str(self.count),sendcity.get_attribute("title"))
            #time.sleep(10)
        except BaseException:
            print ("数据解析异常")
            pass
        else:
            pass





if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # 在Django 里想单独执行文件写上这句话
    django.setup()  # 执行
    #这个导入不能写在头部,要先执行django进行一些环境初始化工作,否则无法初始化
    from mysite.app.taobao import models
    it = item()
    prod = models.TTbShopProd()
   #prods = prod.objects.all()[1:10000]
    for p in range(1,2000000):
        it.doAction("567492771957")
        it.doAction("565923458401")



