# -*- coding: utf-8 -*-
import os
# 导入Django
import django
from mysite.libs import BaseHttpGet

# 测试类
class TestHttpGet(BaseHttpGet.BaseHttpGet):
    url = "http://www.baidu.com/"

    def before(self):
        return False

    def parse(self, response):
        print(response.text)
        return True

if __name__ == '__main__':
    test = TestHttpGet("test")
    test.run()

