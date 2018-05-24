# -*- coding: utf-8 -*-
"""
实现文件int存储，高性能的int查询，添加等操作。
主要针对各种int类型的key判断，存储在缓存中太占内存，存储在数据库中性能较差等问题
1.基于文件指针位置判断，实现1个G可以存储超过1个亿的数字
2.基于byte8位转换，实现更高压缩比，最大情况下1个G的文件可以存放1024*1024*1024*8=8589934592（85亿个数字）
3.基于文件指针，判断，插入，删除，查找都可以毫秒级返回
4.只能存入非负数(0-N)，负数自行转换处理
5.第一位是(0-7)，以此类推
6.由于是文件操作，不允许多线程并发。可以多线程读取判断，但是写入不要多线程进行写入，否则会出现覆盖的情况
"""
import os
import time
from mysite.libs import MyThreadPool
class file_int(object):
    file_path = None #文件存放的路径
    create = True #是否自动创建
    file_hand = None
    def __init__(self,file_path=None,create=True):  # 调用时需传入self相当于this
        if file_path is None:
            raise Exception("file_path is None")
        self.file_path = file_path
        self.create = create
        if create:
            if os.path.isfile(file_path):
                pass
            else:
                #如果不存在，则创建一个空的文件
                os.makedirs(os.path.dirname(file_path),exist_ok=True)
                open(file_path, "w+").close()
        pass

    # 计算1-8位的16进制(高位在前，低位在后)
    def __get_byte_h(self,ste):
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

    # 计算1-8位的16进制,取反(高位在前，低位在后)
    def __get_byte_h2(self,ste):
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

    # 判断byte(8位)，中的某1位是否为1，如果为1，则返回True,否则返回False
    def __has_byte_h(self,b, ste):
        h = self.__get_byte_h(ste)
        ib = int.from_bytes(b, byteorder='big', signed=False)
        # print(ib&h)
        return ib & h == h

    # 添加某位，把byte8位中的某位设置为1,返回设置后的byte
    def __add_byte_h(self,b, ste):
        ib = int.from_bytes(b, byteorder='big', signed=False)
        h = self.__get_byte_h(ste)
        nb = ib | h
        return bytes([nb])

    # 删除某位，把byte8位中的某位设置为0,返回设置后的byte
    def __del_byte_h(self,b, ste):
        h = self.__get_byte_h2(ste)
        ib = int.from_bytes(b, byteorder='big', signed=False)
        return bytes([ib & h])

    #把int存入
    def put_int(self,intv=0,flush=False,close=False):
        if self.file_hand is None:
            self.file_hand = open(self.file_path, "r+b")
        yFile = self.file_hand
        seek = int(intv/8)
        step = intv-seek*8+1
        yFile.seek(seek,os.SEEK_SET)
        rb = yFile.read(1)
        yFile.seek(seek,os.SEEK_SET)
        nb = self.__add_byte_h(rb,step)
        yFile.write(nb)
        if flush:
            yFile.flush()
        if close:
            self.close()
        pass

    # 把int删除
    def del_int(self, intv=0,flush=False,close=False):
        if self.file_hand is None:
            self.file_hand = open(self.file_path, "r+b")
        yFile = self.file_hand
        seek = int(intv/8)
        step = intv-seek*8+1
        yFile.seek(seek,os.SEEK_SET)
        rb = yFile.read(1)
        yFile.seek(seek,os.SEEK_SET)
        nb = self.__del_byte_h(rb,step)
        yFile.write(nb)
        if flush:
            yFile.flush()
        if close:
            self.close()

    #判断是否存在int
    def has_int(self,intv):
        if self.file_hand is None:
            self.file_hand = open(self.file_path, "r+b")
        seek = int(intv / 8)
        step = intv-seek*8+1
        self.file_hand.seek(seek,os.SEEK_SET)
        rb = self.file_hand.read(1)
        return self.__has_byte_h(rb,step)
        pass

    def close(self):
        if self.file_hand is None:
            self.file_hand.close()
            self.file_hand = None




if __name__ == '__main__':
    currtime = time.time()
    fi = file_int("/test/test3/test2")
    for i in range(10000):
        pass
        fi.put_int(i)
        #t.callInThread(test,i)
    fi.close()
    print(time.time()-currtime)
