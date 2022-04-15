from system_manage.utils import permission_required_method
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    '''
    관리자 메인 화면
    김병주/2022.04.13
    '''
    login_url='system_manage:login'
    template_name = 'system_manage/admin_main.html'

    @permission_required_method('read.system_manage', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)
class LoginView(View):
    '''
    관리자 로그인 기능
    김병주/2022.04.13
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('system_manage:home')

        return render(request, 'system_manage/admin_login.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        id = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=id, password=password)

        if user is not None:
            if not (user.is_superuser or str(user.groups.all()[0]) == 'master'):
                context['success'] = False
                context['message'] = '접속 권한이 없습니다.'
                return JsonResponse(context, content_type='application/json')
            login(request, user)
            if 'next' in request.GET:
                url = request.GET.get('next')
                context['url'] = url.split('?next=')[-1]
            context['success'] = True
            context['message'] = '로그인 되었습니다.'
        else:
            context['success'] = False
            context['message'] = '일치하는 회원정보가 없습니다.'
        return JsonResponse(context, content_type='application/json')

class PermissionDeniedView(LoginRequiredMixin, TemplateView):
    login_url = 'system_manage:login'
    template_name='system_manage/permission_denied.html'