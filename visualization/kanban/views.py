from django.shortcuts import render
from django.http import HttpResponse
from django import template

# Create your views here.
def kanban(request):

    return render(request, 'kanban.html')

def VisualTest(request):
    return render(request, 'visual_test.html')