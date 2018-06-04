# -*- coding: utf-8 -*-
'''
测试python的反射的用法
'''


if __name__ == '__main__':
    #1.导入模块（即）
    module = __import__("mysite.app.ipproxy.views",fromlist=True)  #如果不加上fromlist=True,只会导入第一级
    func = getattr(module, 'hello')
    result = func(None,1)
    print(result)
