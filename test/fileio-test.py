# -*- coding: UTF-8 -*-
# 文件数据合并去重处理 2018-01-16
import codecs
import datetime
start = datetime.datetime.now()
srcfile = ['E:/datap/2017/1.txt',
           'E:/datap/2017/2.txt',
            'E:/datap/2017/3.txt',
            'E:/datap/2017/4.txt',
            'E:/datap/2017/5.txt',
            'E:/datap/2017/6.txt',
            'E:/datap/2017/7.txt',
            'E:/datap/2017/8.txt',
            'E:/datap/2017/9.txt',
           'E:/datap/2017/10.txt',
            'E:/datap/2017/11.txt',
            'E:/datap/2017/12.txt',
            'E:/datap/2017/13.txt'
           ]
dictno = {"a":"","key":"value"}

#输出文件
#codecs.open()
fw = codecs.open("D:/temp/TEST.log", "w",'gbk')

for fn in srcfile:  # 第一个实例
    print ('当前文件 :', fn)
    #if(len(fn)<3):continue
    fo = codecs.open(fn, "r",encoding='gbk',errors='ignore')
    print ("正在读取: ", fo.name)

    for line in fo:


        #line2 = line.decode("utf-8")
        line = line.strip().replace("|",",")
        nos =line.split(",")
        if(len(nos)<3):
            continue
        no = nos[1]
        if(len(no)<10 | len(no)>13):
            continue
        if(dictno.has_key(no)):
            dictno[no] = dictno[no]+1
            #continue
        else:
            dictno[no] = 1
        fw.write(line+"\r\n")
        #print(no)
# 关闭打开的文件
fo.close()
usetime =(datetime.datetime.now()-start).seconds
print ("耗时: ", usetime)