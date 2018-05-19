# -*- coding: utf-8 -*-
import requests
import time
from mysite.app.ipproxy import ippool
from mysite.libs import myredis
import pickle

# 所有数据抓取的基类，所有页面的Get形式的抓取，都实现此类
class BaseHttpGet(object):
    id = None
    name = "BaseHttpGet"
    url = None  # 抓取的url
    isProxy = False  # 是否采用代理
    maxThread = 10  # 允许爬虫采用的最大线程
    encoding = 'utf-8'
    # http的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.3'
    }

    # 执行数据爬取 get前调用，如果这个返回False,则整个调用作废掉,默认返回True
    def before(self):
        return True

    # 执行数据爬取 get，如果成功，则调用parse方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def run(self):
        if self.before() is False:
            return True
        # 忽略警告
        requests.packages.urllib3.disable_warnings()
        if self.isProxy:
            try:
                ipm = ippool.popCheckIp()
                while ipm is None:
                    ipm = ippool.popCheckIp()
                    time.sleep(0.1)
                proxy = 'http://' + ipm.host
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
                r = requests.get(self.url, headers=self.headers, proxies=proxies, allow_redirects=True, verify=False)
                r.encoding = self.encoding
                ipm.check_time = int(time.time())
                ipm.errorCount = 0
                ippool.pushCheckIp(ipm)
                return self.parse(r)
            except Exception:
                ipm.errorCount = ipm.errorCount + 1
                # 3次以内，可以继续使用，错误超过3次，则丢弃
                if ipm.errorCount < 3:
                    ippool.pushCheckIp(ipm)
                else:
                    ipm.save()
                pass
                return False
        else:
            try:
                r = requests.get(self.url, headers=self.headers, allow_redirects=True, verify=False)
                r.encoding = self.encoding
                return self.parse(r)
            except Exception:
                pass
                return False

        pass

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        return True
        pass



# 把待爬取的http连接放入到池中
def pushHttpGet(httpget=None):
    r = myredis.getRedis()
    # 先判断池中是否已存在，如果存在，在直接返回
    if httpget.id is not None:
        if r.exists("HTTPGET:ID" + httpget.id):
            return
        #24小时内不重复
        r.set("HTTPGET:ID:" + httpget.id, None, ex=60 * 60 * 24)
    pass
    # 从右边放入队列
    # print("push:"+ipm.host+","+ipm.src_url)
    r.rpush("HTTPGET:POOL", pickle.dumps(httpget))

def popHttpGet():
    r = myredis.getRedis()
    httpget = r.lpop("HTTPGET:POOL")
    if httpget is None:
        return None
    return pickle.loads(httpget)

# 测试类
class TestHttpGet(BaseHttpGet):
    url = "http://www.baidu.com/"

    def before(self):
        return False

    def parse(self, response):
        print(response.text)
        return True


if __name__ == '__main__':
    test = TestHttpGet()
    test.run()
