# -*- coding: utf-8 -*-

#抽取字符串
def ExtStr(src,star,end):
    if src == None:
        return None
    idxs = src.find(star)
    idxe = src.find(end)
    if idxs==-1:
        return None
    else:
        idxs=idxs+len(star)
    if idxe==-1:
        idxe=len(src)
    return src[idxs:idxe]



