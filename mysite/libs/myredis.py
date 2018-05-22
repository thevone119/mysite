# -*- coding: utf-8 -*-
#对redis的封装
#1.对redis连接的封装，共用一个连接
#2.对各种操作进行线程加锁，避免线程锁

import redis
import threading

# 引入锁
L_INIT = threading.Lock()
L_HM = threading.Lock()
L_QUEUE = threading.Lock()
L_OTHER = threading.Lock()

REDIS_POOL = None
#只返回一个公共的连接
def getRedis():
    global REDIS_POOL
    L_INIT.acquire()
    if REDIS_POOL is None:
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
        REDIS_POOL = redis.Redis(connection_pool=pool)
        print("init Redis")
    if REDIS_POOL.ping() is False:
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
        REDIS_POOL = redis.Redis(connection_pool=pool)
        print("reInit Redis")
    L_INIT.release()
    return REDIS_POOL

def hset( name=None, key=None, value=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.hset(name,key,value)
    except Exception as e:
        print("hset错误", e)
        pass
    finally:
        L_HM.release()


def hget( name=None, key=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.hget(name,key)
    except Exception as e:
        print("hget错误", e)
        pass
    finally:
        L_HM.release()


def hdel( name=None, key=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.hdel(name,key)
    except Exception as e:
        print("hdel错误", e)
        pass
    finally:
        L_HM.release()



def rpush( name=None, *values):
    r = getRedis()
    L_QUEUE.acquire()
    try:
        return r.rpush(name,*values)
    except Exception as e:
        print("rpush错误",e )
        pass
    finally:
        L_QUEUE.release()


def lpop( name=None):
    r = getRedis()
    L_QUEUE.acquire()
    try:
        return r.lpop(name)
    except Exception as e:
        print("lpop错误", e)
        pass
    finally:
        L_QUEUE.release()


def hexists(name=None,key=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.hexists(name,key)
    except Exception as e:
        print("hexists错误", e)
        pass
    finally:
        L_HM.release()


def set(name=None,value=None,ex =None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.set(name,value,ex=ex)
    except Exception as e:
        print("set错误", e)
        pass
    finally:
        L_HM.release()

def get(name=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.get(name)
    except Exception as e:
        print("get错误", e)
        pass
    finally:
        L_HM.release()

def exists(name=None):
    r = getRedis()
    L_HM.acquire()
    try:
        return r.exists(name)
    except Exception as e:
        print("exists错误", e)
        pass
    finally:
        L_HM.release()
