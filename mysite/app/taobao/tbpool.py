# -*- coding: utf-8 -*-
# 淘宝数据的缓冲池，所有淘宝相关的数据缓冲池均在此定义

from mysite.libs import myredis
import pickle
import time
import threading

TB_POOL_ISG = "TB:isg"  # 淘宝的isg,cookie存放在这里,先进先出队列,用线程抓取一批isg到这里存储，做备用
TB_POOL_SHOPID = "TB:SHOPID"  # 淘宝的shopid
TB_POOL_PRODID = "TB:PRODID"  # 淘宝的prodid

# 引入锁
L = threading.Lock()

# 放入isg
def pushISG(isg=None):
    myredis.rpush(TB_POOL_ISG, isg)


# 取出isg
def popISG():
    isg = myredis.lpop(TB_POOL_ISG)
    if isg is None:
        return None
    isg = isg.decode()
    return isg


# 判断shopid是否存在，
# 如果存在，则返回True
# 如果不存在，则存入缓存，返回False
def ShopIdExist(shopid=None):
    if myredis.hexists(TB_POOL_SHOPID, shopid):
        return True
    else:
        myredis.hset(TB_POOL_SHOPID, shopid, None)
        return False

def prodIdExist(prodId=None):
    if myredis.hexists(TB_POOL_PRODID, prodId):
        return True
    else:
        myredis.hset(TB_POOL_PRODID, prodId, None)
        return False