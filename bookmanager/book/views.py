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
    context = {
        'name': '特别推荐'
    }

    return render(request, 'books/index.html', context=context)

'''
# ----------增加数据------------
from book.models import BookInfo

# 方式一
book = BookInfo(
    name='Django开发',
    pub_date='2022-10-10',
    readcount='100'
)
# 要调用对象的save方法才能保存到数据库，save方法是django已经内置写好的函数
book.save()

# 方式二
# objects相当于一个代理，可以实现数据的增删查改
BookInfo.objects.create(
    name='系统运维从入门到精通',
    pub_date='2022-3-15',
    readcount=5
)

# ----------修改数据------------
from book.models import BookInfo
# book = BookInfo.objects.get(id=7)
# book.name='Linux shell精通'
# book.save()

BookInfo.objects.filter(name='Django').update(name='PYQT精通')
'''

from book.models import BookInfo
book = BookInfo.objects.get(name='精通PYQT')