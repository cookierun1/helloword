from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse

# Create your views here.
class HomeView(TemplateView):
    '''
    사용자 메인 화면
    김병주/2022.04.14
    '''
    template_name = 'user/user_main.html'
