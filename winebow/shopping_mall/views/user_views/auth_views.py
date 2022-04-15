from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login


class HomeView(TemplateView):
    '''
    사용자 메인 화면
    김병주/2022.04.14
    '''
    template_name = 'user/user_main.html'

class LoginView(View):
    '''
    로그인 기능
    김병주/2022.04.15
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.id:
            return redirect('shopping_mall:home')

        return render(request, 'user/user_login.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        id = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=id, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                context['url'] = request.GET.get('next')
            context['success'] = True
            context['message'] = '로그인 되었습니다.'
        else:
            context['success'] = False
            context['message'] = '일치하는 회원정보가 없습니다.'
        return JsonResponse(context, content_type='application/json')