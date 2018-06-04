# -*- coding: utf-8 -*-
'''
jinja2是Flask作者开发的一个模板系统，起初是仿django模板的一个模板引擎，为Flask提供模板支持，由于其灵活，快速和安全等优点被广泛使用。
测试如何使用Jinja2的模板引擎生成文件
1.用str(字符串做模板)，生成字符串
2.用文件做模板，生成字符串

'''
from jinja2 import Template, Environment, PackageLoader,FileSystemLoader


def test1():
    '''
    直接使用模板进行加载，字符串模板，输出字符串
    :return:
    '''
    context = {'name': '我是模板', 'list': range(10)}
    template = Template('Hello {{ name }}!')
    content = template.render(context, name="123")
    print(content)

def test2():
    '''
    使用环境加载，通过包加载的方式加载模板，采用文件模板，输出字符串

    :return:
    '''
    env = Environment(loader=FileSystemLoader('d:/p_work/mysite/templates')) #这是文件系统加载器，不需要在包下，只用用文件的形式加载
    env = Environment(loader=PackageLoader('mysite')) #这是包加载器，通过包下进行加载,但是一般的web项目模板文件一般不放在包下。所以这个就比较烦人了
    template = env.get_template('hello/index.html')
    context = {'name': '我是模板', 'list': range(10)}
    content = template.render(context, name="123")
    print(content)

if __name__ == '__main__':
    test2()
