from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from shopping_mall.tokens import account_activation_token
from django.core.validators import RegexValidator
from validate_email import validate_email
from django.contrib.auth.models import User, Group
from config.models import Profile

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
        if request.user.is_authenticated:
            return redirect('shopping_mall:home')
        str = 'qudwn1114@gmal.co'
        print(validate_email(str))
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

class RegisterView(View):
    '''
    회원가입 기능, 이메일 전송
    김병주/2022.04.15
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('shopping_mall:home')
        return render(request, 'user/user_register.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        id = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['confirm-password']
        email = request.POST['email']
        if not validate_username(id):
            context['success'] = False
            context['message'] = "유효하지 않은 사용자 이름입니다."
            return JsonResponse(context, content_type="application/json")
        if not validate_password(password):
            context['success'] = False
            context['message'] = "유효하지 않은 비밀번호입니다."
            return JsonResponse(context, content_type="application/json")
    
        if not validate_email(email):
            context['success'] = False
            context['message'] = "유효하지 않은 이메일 주소입니다."
            return JsonResponse(context, content_type="application/json")

        if password != password_confirm:
            context['success'] = False
            context['message'] = '비밀번호가 일치하지 않습니다.'
            return JsonResponse(context, content_type='application/json')

        try:
            user = User.objects.get(username=id)
            context['success'] = False
            context['message'] = '아이디가 이미 존재합니다.'
            return JsonResponse(context, content_type='application/json')
        except:
            pass
        
        try:
            user = User.objects.get(email=email)
            context['success'] = False
            context['message'] = '이미 가입한 이메일 입니다.'
            return JsonResponse(context, content_type='application/json')
        except:
            print('이메일 사용 가능')
            user = User.objects.create_user(
                id,
                email,
                password
            )
            user.is_active = False
            user.save()
            userid = user.id
            
        current_site = get_current_site(request) 
        message = render_to_string('user/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        mail_title = "계정 활성화 확인 이메일"
        sendEmail = EmailMessage(mail_title, message, settings.EMAIL_HOST_USER, to=[email])
        print("이메일 전송: ", sendEmail.send())
        default_group, _ = Group.objects.get_or_create(name=settings.DEFAULT_GROUP)
        user.groups.add(default_group.id)

        context['success'] = True
        context['message'] = '가입 되었습니다.'
        return JsonResponse(context, content_type='application/json')

def activate(request: HttpRequest, uidb64, token):
    '''
    토큰 인증을 통한 계정 활성화
    김병주/2022.04.18
    '''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        profile = user.profile
        profile.email_verified = '1'
        profile.save()
        return render(request, 'user/activation_complete.html', {'username' : user.username})
    else:
        return render(request, 'user/activation_error.html', {'error' : '만료 된 링크입니다.'})

class ConfirmEmailView(View):
    '''
    이메일 보냄 확인 페이지
    김병주/2022.04.15
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        email = request.GET.get('email', '')
        context['email'] = email

        return render(request, 'user/confirm_email.html', context)



def validate_username(username):
    '''
    아이디 유효성 체크
    김병주/2022.04.19
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9]{6,20}$')(username)
    except:
        return False

    return True

def validate_password(password):
    '''
    비밀번호 유효성 체크
    김병주/2022.04.19
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9!@#$%^&*()+.,~]{8,16}$')(password)
    except:
        return False

    return True

def validate_username(username):
    '''
    이메일 유효성 체크
    김병주/2022.04.19
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9]{6,20}$')(username)
    except:
        return False

    return True