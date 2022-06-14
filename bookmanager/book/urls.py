from django.contrib import admin
from django.urls import path
from book.views import index
from django.urls import include

# urlpatterns= [] 是固定写法
urlpatterns =[
    #path路由，视图函数名
   path('index/', index)
]