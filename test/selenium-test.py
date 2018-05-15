# -*- coding:utf-8 -*-
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2,"permissions.default.stylesheet":2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
#webdriver.PhantomJS
#diver=webdriver.Chrome()
#Chrome_login=webdriver.

#打开网址
driver.get('https://www.baidu.com/')
driver.maximize_window()#窗口最大化，可有可无，看情况

#输入账户密码
#我请求的页面的账户输入框的'id'是username和密码输入框的'name'是password
inp = driver.find_element_by_xpath('//*[@id="kw"]')
inp.clear()
inp.send_keys("test123213")
#输入完后点击搜索

driver.find_element_by_xpath('//*[@id="su"]').click()

#刷新
driver.refresh()
title = driver.execute_script("return document.title")
print(title)

inp = driver.find_element_by_xpath('//*[@id="kw"]')
inp.clear()
inp.send_keys("test2")
#输入完后点击搜索
driver.find_element_by_xpath('//*[@id="su"]').click()
cookies = driver.get_cookie("BAIDUID")
title = driver.execute_script("return document.title")#js
print(title)

#浏览器退出
#firefox_login.quit()
