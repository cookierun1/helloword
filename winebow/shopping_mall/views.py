from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse

# Create your views here.
class HomeView(TemplateView):
    '''
    관리자 메인 화면
    김병주/2022.04.13
    '''
    template_name = 'user_main.html'
