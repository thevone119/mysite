# -*- coding: utf-8 -*-
'''
定义活动的url,实现所有url均通过此方法进行转发，指定固定的url规则，通过约定大于配置的方式，使用约定的方式进行url转发。
采用反射的机制实现url的映射，不用每个url都配置
1.所有url都是/app/app名称/func名称/参数1/参数2/参数3/参数4...的格式。
2.前3级是app,app名称，views下的函数名称。
3.后面更多的则是各种参数,按顺序传入。
'''

from django.shortcuts import render_to_response,HttpResponse,redirect


def activity_url_process(request, **kwargs):
    '''接收所有匹配url的请求，根据请求url中的参数，通过反射动态指定view中的方法'''
    print("请求url:"+request.path)
    pars = request.path.split("/")
    if len(pars)<3:
        return HttpResponse('404 Not Found')
    appname = pars[2]
    funcname = pars[3]
    print("appname:",appname,"funcname",funcname)

    try:
        appObj = __import__("mysite.app."+appname+".views")
        viewObj = getattr(appObj, 'views')
        funcObj = getattr(viewObj, funcname)

        # 执行view.py中的函数，并获取其返回值
        result = funcObj(request, kwargs)

    except ImportError:
        # 导入失败时，自定义404错误
        return HttpResponse('404 Not Found')
    except AttributeError:
        # 导入失败时，自定义404错误
        return HttpResponse('404 Not Found')
    except Exception as e:
        # 代码执行异常时，自动跳转到指定页面
        #return redirect('/app01/index/')
        return HttpResponse('503 Not Found')
    return result