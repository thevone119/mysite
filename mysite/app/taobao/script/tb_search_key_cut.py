# -*- coding: utf-8 -*-
"""
针对淘宝的商店名称，商品名称实现分词
方便对各种搜索实现更强大的搜索
1.店铺名称分词（保留1万个分词）
2.商品名称分词（保留10万个分词）
分词内容保存在缓存中
分词器使用jieba分词器
"""
import jieba

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

#淘宝商店名称分词
def cat_shop_name():
    dict = {}
    #取100万个店铺名称做分词，保留1万个分词结果
    for i in range(100):
        print(len(dict))
        start=i*1000
        list = models.TTbShop.objects.all()[start:start+1000]
        for shop in list:
            if shop.title is None:
                continue
            cut = jieba.cut(shop.title)
            for c in cut:
                if len(c)>2:
                    continue
                if c in dict:
                    dict[c]=dict[c]+1
                else:
                    dict[c] = 1


    slist = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    for l in slist:
        pass
        print(l[0],l[1])

if __name__ == '__main__':

    cat_shop_name()
