from django.urls import path
from book.views import create_book,shop, register,my_json
from book.views import set_cookie,get_cookie,set_session,get_session,LoginView

urlpatterns = [

    path('create/', create_book),
    path('<int:city_id>/<int:shop_id>/', shop),

    # django提示post请求尾不能有斜杠
    path('register', register),
    path('json/', my_json),
    path('set_cookie/', set_cookie),
    path('get_cookie/', get_cookie),
    path('set_session/', set_session),
    path('get_session/', get_session),
    # django提示post请求尾不能有斜杠
    path('163login', LoginView.as_view()),
]