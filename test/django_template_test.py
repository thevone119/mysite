# -*- coding: utf-8 -*-
'''
测试如何使用django的模板引擎生成文件
1.用str(字符串做模板)，生成字符串
2.用文件做模板，生成字符串

测试发现用django的模板，依赖django的环境，单独运行比较麻烦。
还是用Jinja2模板引擎比较好，很多web框架也支持此模板引擎，比django的更通用了
'''
from django.template import loader
import django.template
if __name__ == '__main__':
    context = {'title': '我是模板', 'list': range(10)}

    temp = django.template.Template("html fom mat", None)

    content = temp.render(context)
    print(content)
