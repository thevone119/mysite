# -*- coding: UTF-8 -*-
# 文件数据合并去重处理 2018-01-16
import codecs
import datetime
import array
open("d:/testio", "w+b").close()
yFile = open("d:/testio", "r+b")

b=  yFile.read(1)




#计算1-8位的16进制(高位在前，低位在后)
def get_byte_h(ste):
    if ste == 1:
        return 0x80
    if ste == 2:
        return 0x40
    if ste == 3:
        return 0x20
    if ste == 4:
        return 0x10
    if ste == 5:
        return 0x08
    if ste == 6:
        return 0x04
    if ste == 7:
        return 0x02
    if ste == 8:
        return 0x01

#计算1-8位的16进制,取反(高位在前，低位在后)
def get_byte_h2(ste):
    if ste == 1:
        return 0x7f
    if ste == 2:
        return 0xbf
    if ste == 3:
        return 0xdf
    if ste == 4:
        return 0xef
    if ste == 5:
        return 0xf7
    if ste == 6:
        return 0xfb
    if ste == 7:
        return 0xfd
    if ste == 8:
        return 0xfe

#判断byte(8位)，中的某1位是否为1，如果为1，则返回True,否则返回False
def has_byte_h(b,ste):
    h = get_byte_h(ste)
    ib = int.from_bytes(b,byteorder='big',signed=False)
    #print(ib&h)
    return ib&h==h

#添加某位，把byte8位中的某位设置为1,返回设置后的byte
def add_byte_h(b,ste):
    ib = int.from_bytes(b, byteorder='big', signed=False)
    h = get_byte_h(ste)
    nb = ib | h
    return bytes([nb])

#删除某位，把byte8位中的某位设置为0,返回设置后的byte
def del_byte_h(b,ste):
    h = get_byte_h2(ste)
    ib = int.from_bytes(b,byteorder='big',signed=False)
    return bytes([ib & h])


print(len(b))
print(int.from_bytes(b,byteorder='big',signed=False))
print(del_byte_h(b,1))
for i in range(1,9):
    print(has_byte_h(b,i))

#yFile.flush()
#yFile.close()


