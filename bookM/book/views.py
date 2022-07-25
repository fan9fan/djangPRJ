from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from book.models import BookInfo
import json

# Create your views here.
def create_book(request):
    # book = BookInfo.objects.create(
    #     name= '定位',
    #     pub_date= '2020-1-22',
    #     readcount= 99,
    # )
    return HttpResponse('Hello Python!!!')

def shop(request, city_id, shop_id):

    return HttpResponse('Welcome to FADA STORE')

def register(request):
    data = request.POST
    print(data)

    return HttpResponse('Register Successfull')


def my_json(request):
    # 获得json字典
    body = request.body
    # 将json字典转换成python字典--->相当于对收到的json数据解码
    json_dir = json.loads(body)
    print(json_dir)


    return HttpResponse('JJJJSON')


def set_cookie(request):
    # get username
    username = request.GET.get("username")
    password = request.GET.get("password")

    #服务器设置cookie信息
    # 通过响应对象.set_cookie方法
    response = HttpResponse('set_cookie')

    response.set_cookie('name', username)
    response.set_cookie('pwd', password)

    return response

def get_cookie(request):

    name = request.COOKIES.get('name')

    return HttpResponse(name)


def set_session(request):
    username = request.GET.get('username')
    user_id = 1

    request.session['user_id'] = user_id
    request.session['username'] = username

    return HttpResponse('set_session')


def get_session(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    content = '{},{}'.format(user_id, username)

    return HttpResponse(content)

class LoginView(View):
    def get(self, request):

        return HttpResponse('get/get/get')

    def post(self, request):
        return HttpResponse('post/post/post')

