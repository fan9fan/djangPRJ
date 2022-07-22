from django.urls import path
from kanban.views import kanban,VisualTest

urlpatterns = [
    path('kanban/', kanban),
    path('visual/', VisualTest)
]