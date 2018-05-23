# -*- coding: utf-8 -*-
import requests
import time
from mysite.app.ipproxy import ippool
from mysite.app.ipproxy import models
from mysite.libs import myredis
import pickle
import http.client
import json
import queue
import threading


# 引入锁
THREAD_L = threading.Lock()
HTTP_POOL = None
#记录最后初始化的时间，2分钟重新生成连接池
HTTP_POOL_TIME = int(time.time())

def getSessionPool():
    global HTTP_POOL,HTTP_POOL_TIME
    max_connect = 20
    #同步代码块
    THREAD_L.acquire()
    #如果是空的，初始化连接，如果超过5000次请求，也重新初始化连接
    if HTTP_POOL is None:
        HTTP_POOL = queue.Queue(0)
        requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        for i in range(max_connect):
            HTTP_POOL.put(requests.Session())
    if time.time()-HTTP_POOL_TIME > 60*2:
        print("--------------重新初始化HTTP连接池连接------------------------")
        HTTP_POOL_TIME = int(time.time())
        requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        for i in range(max_connect):
            s = HTTP_POOL.get()
            s.close()
            HTTP_POOL.put(requests.Session())
    THREAD_L.release()
    s = HTTP_POOL.get()
    HTTP_POOL.put(s)
    return s

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

    def __init__(self):  # 调用时需传入self相当于this

        pass

    # 执行数据爬取 get前调用，如果这个返回False,则整个调用作废掉,默认返回True
    def before(self):
        return True

    # 对int进行处理
    def paseInt(self,v=None):
        if v is None:
            return None
        try:
            return int(v)
        except:
            pass
        return None

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
                requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
                r = requests.get(self.url, headers=self.headers, proxies=proxies, allow_redirects=True, verify=False)
                r.encoding = self.encoding
                ipm.check_time = int(time.time())
                ipm.errorCount = 0
                ippool.pushCheckIp(ipm)
                return self.parse(r)
            except Exception as e:
                print("代理异常",ipm.host,e)
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

                #requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
                #http.client.HTTPConnection._http_vsn = 10
                #http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
                s = getSessionPool()

                r = s.get(self.url, headers=self.headers, allow_redirects=True, verify=False)
                r.encoding = self.encoding
                return self.parse(r)
            except Exception as e:
                print("BaseHttpGet run 错误",e)
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
    # 先判断池中是否已存在，如果存在，在直接返回
    if httpget.id is not None:
        if myredis.hexists("HTTPGET_ID" , httpget.id):
            return
        else:
            myredis.hset("HTTPGET_ID",httpget.id,None)
    pass
    # 从右边放入队列
    # print("push:"+ipm.host+","+ipm.src_url)
    n = "HTTPGET:"+httpget.__class__.__name__
    myredis.rpush("HTTPGET:"+httpget.__class__.__name__, pickle.dumps(httpget))


# 把待爬取的http连接从池中取出
def popHttpGet(cls=None):
    hg = myredis.lpop("HTTPGET:"+cls.__name__)
    if hg is None:
        return None
    hg = pickle.loads(hg)
    if hg.id is not None:
        myredis.hdel("HTTPGET_ID",hg.id)
    return hg

#把待爬取的http连接池的总容量（某个类型对象的容量）
def getHttpGetPoolCount(cls=None):
    c = myredis.llen("HTTPGET:"+cls.__name__)
    if c is None:
        return 0
    return int(c)

# 测试类
class TestHttpGet(BaseHttpGet):
    url = "https://www.baidu.com"
    def before(self):
        return False

    def parse(self, response):
        print(response.text)
        return True


if __name__ == '__main__':
    test = TestHttpGet()
    pushHttpGet(test)
    test2 = popHttpGet()
    print(test.url)

    pass


