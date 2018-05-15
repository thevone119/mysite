# -*- coding: utf-8 -*-
import redis



def getRedis():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
    r = redis.Redis(connection_pool=pool)
    return r
