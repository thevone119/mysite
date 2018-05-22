# -*- coding: utf-8 -*-

from mysite.libs import BaseHttpGet
import json


if __name__ == '__main__':
    test = BaseHttpGet.TestHttpGet()
    test.url = "https://www.baidu.com"
    test.name = "中文来了"
    test.run()
    print(test.url)
    jtxt = json.dumps(test, default=lambda o: o.__dict__, ensure_ascii=False)
    print(jtxt)
    test2 = json.loads(jtxt)
    test3 = BaseHttpGet.TestHttpGet()
    test3.__dict__ = test2
    print(test3.name)
    pass