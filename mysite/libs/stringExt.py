# -*- coding: utf-8 -*-
import urllib.parse
#字符串抽取类
class StringExt(object):
    src = None
    lines = None

    def __init__(self,src=None):  # 调用时需传入self相当于this
        self.src = src
        pass

    # 抽取字符串
    def ExtStr(self, star, end=None):
        if self.src is None:
            return StringExt(None)
        idxs = self.src.find(star)
        if idxs == -1:
            return StringExt(None)
        else:
            idxs = idxs + len(star)
        if end is None:
            return StringExt(self.src[idxs:])
        idxe = self.src.find(end,idxs)
        if idxe == -1:
            idxe = len(self.src)
        return StringExt(self.src[idxs:idxe])

    # 抽取字符串
    def extractLine(self, *args,beg=0):
        if self.src is None:
            return StringExt()
        if self.lines is None:
            self.lines = self.src.split("\n")
        _lines = self.lines
        if beg>0:
            _s = self.src[beg:]
            _lines = _s.split("\n")

        for l in _lines:
            l = l.strip()
            if len(l) < 1:
                continue
            isf = True
            for value in args:
                if l.find(value) < 0:
                    isf = False
                    break
            if isf:
                return StringExt(l)
        pass
        return StringExt(None)

    def str(self):
        return self.src

    def int(self):
        if self.src is None:
            return None
        try:
            return int(self.src)
        except:
            pass
        return None

    def float(self):
        if self.src is None:
            return None
        try:
            return float(self.src)
        except:
            pass
        return None

    def indexCount(self,idxstr):
        count=0
        idx = self.src.find(idxstr,0)
        while idx>-1:
            count = count+1
            idx = self.src.find(idxstr,idx+1)
        return count

if __name__ == '__main__':
    st = "123456\n" \
         "fasljdflasdj"

    print(st.find("f",8))
    print(StringExt(st).extractLine("f").str())
    print(StringExt("8.3f").float())
    str = "%E6%B0%B4%E6%99%B6%E9%9D%88"
    print(urllib.parse.unquote(str))