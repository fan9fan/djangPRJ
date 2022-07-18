from django.urls import path
from apps.goods.views import IndexView, ListView, SKUSearch, CategoryVisitCountView
urlpatterns = [
    path('index/', IndexView.as_view()),
    path('list/<category_id>/skus/', ListView.as_view()),
    path('search/', SKUSearch()),
    path('detail/visit/<category_id>/',CategoryVisitCountView.as_view()),
]