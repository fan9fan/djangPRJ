from django.shortcuts import render

# Create your views here.
'''
所谓视图就是python的函数
视图函数做两件事：
1.接收请求，这个请求是django内置的HttpRquest类对象
2.对请求作出回应，这个回应就是django内置的HttpResponse
'''
# 导入视图函数
from django.http import HttpRequest
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello dears friend')