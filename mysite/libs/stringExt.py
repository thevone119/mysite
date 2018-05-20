# -*- coding: utf-8 -*-

#抽取字符串
def ExtStr(src,star,end=None):
    if src == None:
        return None
    idxs = src.find(star)
    if idxs==-1:
        return None
    else:
        idxs=idxs+len(star)
    if end is None:
        return src[idxs:]
    idxe = src.find(end)
    if idxe==-1:
        idxe=len(src)
    return src[idxs:idxe]

#抽取字符串
def extractLine(src,*args):
    if src == None:
        return None
    sline = src.split("\n")
    for l in sline:
        l = l.strip()
        if len(l) < 1:
            continue
        isf = True
        for value in args:
            if l.find(value) < 0:
                isf = False
                break
        if isf:
            return l
    pass
    return None

#对int进行处理
def paseInt(v=None):
    if v is None:
        return None
    try:
        return int(v)
    except :
        pass
    return None


if __name__ == '__main__':
    st = "123456\n" \
         "fasljdflasdj"
    print(extractLine(st,"fas",'lj'))