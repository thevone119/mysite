# -*- coding: utf-8 -*-
# 淘宝数据的缓冲池，所有淘宝相关的数据缓冲池均在此定义

from mysite.libs import myredis
import pickle
import time

TB_POOL_ISG = "TB:isg"  # 淘宝的isg,cookie存放在这里,先进先出队列,用线程抓取一批isg到这里存储，做备用
TB_POOL_EXIST = "TB:EX:"  # 判断是否重复，存放48小时


# 放入isg
def pushISG(isg=None):
    r = myredis.getRedis()
    r.rpush(TB_POOL_ISG, isg)


# 取出isg
def popISG():
    r = myredis.getRedis()
    isg = r.lpop(TB_POOL_ISG)
    isg = isg.decode()
    return isg


# 判断是否存在，
# 如果存在，则返回True
# 如果不存在，则存入缓存，返回False
def existKey(k=None):
    r = myredis.getRedis()
    key = TB_POOL_EXIST + str(k)
    if r.exists(key):
        return True
    else:
        r.set(key, None, ex=60 * 60 * 24 * 2)
    return False
