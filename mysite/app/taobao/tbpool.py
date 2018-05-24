# -*- coding: utf-8 -*-
# 淘宝数据的缓冲池，所有淘宝相关的数据缓冲池均在此定义

from mysite.libs import myredis
import pickle
import time
import threading
from mysite.libs import file_int

TB_POOL_ISG = "TB:isg"  # 淘宝的isg,cookie存放在这里,先进先出队列,用线程抓取一批isg到这里存储，做备用
TB_NO_LIGIN_COOKIE = "TB:NO_LIGIN_COOKIE"  # 淘宝的cookie存放在这里,先进先出队列,用线程抓取一批cookie到这里存储，做备用


#定义2个文件,存放淘宝的商店ID和产品ID.避免数据的重复抓取
F_SHOP_ID = file_int.file_int("/temp/tb_shopid.intf")
F_PROD_ID = file_int.file_int("/temp/tb_prodid.intf")

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
        F_SHOP_ID.put_int(shopid,flush=True)
        return False

def prodIdExist(prodId=None):
    if F_PROD_ID.has_int(prodId):
        return True
    else:
        F_PROD_ID.put_int(prodId,flush=True)
        return False