# -*- coding: utf-8 -*-
#获取淘宝的常用字

from mysite.app.taobao import models
import base64

def encrypt(key, s):
    b = bytearray(str(s).encode("utf-8"))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")

def decrypt(key, s):
    c = bytearray(str(s).encode("utf-8"))
    n = len(c) # 计算 b 的字节数
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("utf-8")
    except:
        return "failed"

if __name__ == '__main__':
    copyright = 'Copyright (c) 2012 Doucube Inc. All rights reserved.'
    # 转成bytes string
    bytesString = encrypt(12,copyright)
    print(decrypt(12,bytesString))



    dictcount = {}
    list = models.TTbShop.objects.all()[0:50000]
    #do_http()
    for shop in list:
        if shop.title is None:
            continue
        for k in shop.title:
            k = k.strip()
            if k is None:
                continue
            if len(k) == 0:
                continue

            bytesString = encrypt(12,k)
            # base64 编码




            if bytesString in dictcount:
                dictcount[bytesString] = dictcount[bytesString] + 1
            else:
                dictcount[bytesString] = 1
            try:
                pass

            except BaseException:
                 pass

    print(len(dictcount))
    slist = sorted(dictcount.items(), key=lambda x:x[1], reverse=True)
    for l in slist:
        pass
        print(decrypt(12,l[0]))



    pass