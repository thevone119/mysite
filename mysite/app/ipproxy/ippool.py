# -*- coding: utf-8 -*-

from mysite.libs import myredis
import pickle
import time

# ip池的控制。这里包含2个池,这里只实现ip池的放入，取出
# 1.未验证的ip池，抓取到的ip直接放入这个池
# 2.已验证的ip池，可用的代理ip放入这个池

IPPROXY_POOL_NO_CHECK = "IP_POOL:NO_CHECK"  # 未检测的池
IPPROXY_POOL_CHECK = "IP_POOL:CHECK"  # 已检测的池，可用的IP池
IPPROXY_POOL_KEY = "IP_POOL:KEY"  # 判断ip是否存在的KEY

IPPROXY_POOL_ERROR_KEY = "IP_Exists:"  # 错误的IP，30分钟不加入进来


# 放入池中,放入队列的末尾
def pushNoCheckIp(ipm=None):
    r = myredis.getRedis()

    # 先判断池中是否已存在，如果存在，在直接返回
    if r.hexists(IPPROXY_POOL_KEY, ipm.host):
        return

    # 先判断池中是否已存在，如果存在，在直接返回
    if r.exists(IPPROXY_POOL_ERROR_KEY + ipm.host):
        return
    r.hset(IPPROXY_POOL_KEY, ipm.host, None)

    # 30分钟内，不重复加入
    r.set(IPPROXY_POOL_ERROR_KEY + ipm.host, None, ex=60 * 30)

    # 从右边放入队列
    # print("push:"+ipm.host+","+ipm.src_url)
    r.rpush(IPPROXY_POOL_NO_CHECK, pickle.dumps(ipm))


# 池中取出，先进先出,如果池中没有，则阻塞
def popNoCheckIp():
    r = myredis.getRedis()
    ipm = r.lpop(IPPROXY_POOL_NO_CHECK)
    while ipm is None:
        time.sleep(0.1)
        ipm = r.lpop(IPPROXY_POOL_NO_CHECK)
    ipm = pickle.loads(ipm)
    # 取出后，删除key
    r.hdel(IPPROXY_POOL_KEY, ipm.host)

    return ipm


# 放入池中,放入队列的末尾,循环利用
def pushCheckIp(ipm=None):
    r = myredis.getRedis()
    r.hset(IPPROXY_POOL_KEY, ipm.host, None)
    # 从右边放入队列
    r.rpush(IPPROXY_POOL_CHECK, pickle.dumps(ipm))


# 池中取出，先进先出,如果池中没有，则阻塞
def popCheckIp():
    r = myredis.getRedis()
    ipm = r.lpop(IPPROXY_POOL_CHECK)
    while ipm is None:
        time.sleep(0.1)
        ipm = r.lpop(IPPROXY_POOL_CHECK)
    ipm = pickle.loads(ipm)
    # 取出后，删除key
    r.hdel(IPPROXY_POOL_KEY, ipm.host)
    return ipm


if __name__ == '__main__':
    for i in range(1):
        print(popNoCheckIp())
