# -*- coding: utf-8 -*-
# 淘宝数据的缓冲池，所有淘宝相关的数据缓冲池均在此定义

from mysite.libs import myredis
import pickle
import time
import threading
from mysite.libs import file_int

TB_POOL_ISG = "TB:isg"  # 淘宝的isg,cookie存放在这里,先进先出队列,用线程抓取一批isg到这里存储，做备用
TB_POOL_PROD_ID = "TB:PROD_ID"  # 淘宝的商品ID，如果不在523839458288  570519703363
TB_POOL_SHOP_ID = "TB:SHOP_ID"  # 淘宝的商品ID，如果不在523839458288  570519703363
TB_NO_LIGIN_COOKIE = "TB:NO_LIGIN_COOKIE"  # 淘宝的cookie存放在这里,先进先出队列,用线程抓取一批cookie到这里存储，做备用


#定义2个文件,存放淘宝的商店ID和产品ID.避免数据的重复抓取
F_SHOP_ID = file_int.file_int("/temp/tb_shopid.intf")
#由于产品ID是在太大，只把100亿左右放到这里
F_PROD_ID = file_int.file_int("/temp/tb_prodid.intf",maxint=1024*1024*1024*8*10)

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

#放入未登陆的cookie
def pushNoLoginCookie(cookie):
    myredis.rpush(TB_NO_LIGIN_COOKIE, cookie)

#取出未登陆的cookie
def popNoLoginCookie():
    cookie = myredis.lpop(TB_NO_LIGIN_COOKIE)
    if cookie is None:
        return None
    cookie = cookie.decode()
    return cookie



# 判断shopid是否存在，
# 如果存在，则返回True
# 如果不存在，则存入缓存，返回False
def ShopIdExist(shopid=None):
    if F_SHOP_ID.has_int(shopid):
        return True
    else:
        F_SHOP_ID.put_int(shopid,flush=False)
        return False

def prodIdExist(prodId=None):
    if prodId>500000000000 and prodId<570000000000:
        prodId = int(str(prodId)[1:])
        if F_PROD_ID.has_int(prodId):
            return True
        else:
            F_PROD_ID.put_int(prodId, flush=False)
            return False
    if myredis.hexists(TB_POOL_PROD_ID,prodId):
        return True
    else:
        myredis.hset(TB_POOL_PROD_ID,prodId,None)
        return False


if __name__ == '__main__':
    prodId = 503839458288
    if prodId > 500000000000 and prodId < 570000000000:
        prodId = int(str(prodId)[1:])
        print(prodId)
