from django.views.generic import View, TemplateView
from django.http.request import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from system_manage.models import Summernote
from django.core import serializers
from system_manage.forms import BoardForm

class EditorSampleView(LoginRequiredMixin, View):
    """
    Editor 페이지 로드.
    김병주/2022.04.29
    """
    login_url='system_manage:login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        paginate_by = '20'
        page = request.GET.get('page', '1')        
        board_list = Summernote.objects.all()
        paginator = Paginator(board_list, paginate_by)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = 1
            page_obj = paginator.page(page)
        except InvalidPage:
            page = 1
            page_obj = paginator.page(page)
        pagelist = paginator.get_elided_page_range(page, on_each_side=3, on_ends=1)
        context['pagelist'] = pagelist

        context['board_list'] = page_obj
        context['page_obj'] = page_obj

        return render(request, 'example/editor_sample.html', context)

class EditorSampleCreateView(LoginRequiredMixin, View):
    '''
    Editor Data Create
    김병주/2022.05.01
    '''
    login_url='system_manage:login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['form'] = BoardForm
        return render(request, 'example/editor_sample_create.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        title = request.POST['title']
        content = request.POST['content']
        Summernote.objects.create(
            title = title,
            content = content,
            auth_user = request.user
        )

        context['success'] = True
        context['message'] = '등록 되었습니다.'
        return JsonResponse(context, content_type='application/json')

class EditorSampleDetailView(LoginRequiredMixin, View):
    '''
    Editor Sample Deatil 및 삭제
    김병주/2022.05.01
    '''
    login_url='system_manage:login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Summernote, pk=kwargs.get('pk'))
        context['data'] = data
        return render(request, 'example/editor_sample_detail.html', context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Summernote, pk=kwargs.get('pk'))
        data.delete()

        context['success'] = True
        context['message'] = '삭제되었습니다.'

        return JsonResponse(context, content_type='application/json')

class EditorSampleEditView(LoginRequiredMixin, View):
    '''
    Editor Sample Edit
    김병주/2022.05.01
    '''
    login_url='system_manage:login'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Summernote, pk=kwargs.get('pk'))
        context['form'] = BoardForm(instance=data)
        
        return render(request, 'example/editor_sample_edit.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        pk=kwargs.get('pk')
        data = get_object_or_404(Summernote, pk=pk)
        title = request.POST['title']
        content = request.POST['content']
        
        data.title = title
        data.content = content
        data.save()

        context['data_id'] = pk
        context['success'] = True
        context['message'] = '수정 되었습니다.'
        return JsonResponse(context, content_type='application/json')