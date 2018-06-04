from django.shortcuts import render

# Create your views here.

'''
   定义了一个试图函数
   requset ： 请求的request
   '''
def hello(request,p1=None,p2=None,p3=None):
    print("进入了hello",p1)
    # 传递给模板的数据
    context = {'title': '我是模板', 'list': range(10)}
    return render(request, 'hello/index.html', context)
    # return HttpResponse("你好，我是模块！")