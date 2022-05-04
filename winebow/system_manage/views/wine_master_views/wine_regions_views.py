import re
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
import os, json

from system_manage.utils import permission_required_method
from system_manage.models import Region

class WineRegionView(LoginRequiredMixin, View):
    '''
    와인 지역 정보 관리
    김병주/2022.04.22
    '''
    login_url='system_manage:login'
    @permission_required_method('read.wine_region', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        paginate_by = '20'
        page = request.GET.get('page', '1')
        search_type = self.request.GET.get('search_type', '')
        search_keyword = self.request.GET.get('search_keyword', '')
        if search_keyword:
            context['search_type'] = search_type
            context['search_keyword'] = search_keyword
            if search_type == 'name_kr':
                region = Region.objects.filter(regionNameKr__icontains=search_keyword)
            elif search_type == 'name_en':
                region = Region.objects.filter(regionNameEn__icontains=search_keyword)
        else:
            region = Region.objects.all()

        paginator = Paginator(region, paginate_by)

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

        context['region'] = page_obj
        context['page_obj'] = page_obj
        return render(request, 'wine_master/wine_region/wine_region.html', context)

class WineRegionCreateView(LoginRequiredMixin, View):
    '''
    와인 지역 Create
    김병주/2022.04.25
    '''
    login_url='system_manage:login'
    @permission_required_method('read.wine_region', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, 'wine_master/wine_region/wine_region_create.html', context)

    @permission_required_method('write.wine_region', raise_exception=True)
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        name_kr = request.POST['name_kr']
        name_en = request.POST['name_en']
        image = request.FILES.get('image', None)
        description = request.POST['description']
        region = Region.objects.create(
            regionNameKr = name_kr,
            regionNameEn = name_en,
            regionDes = description
        )
        if image:
            region.regionImg = image
            region.save()

        context['success'] = True
        context['message'] = '등록 되었습니다.'
        return JsonResponse(context, content_type='application/json')

class WineRegionDetailView(LoginRequiredMixin, View):
    '''
    와인 지역 Deatil 및 삭제
    김병주/2022.04.25
    '''
    login_url='system_manage:login'
    @permission_required_method('read.wine_region', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        context['data'] = data
        return render(request, 'wine_master/wine_region/wine_region_detail.html', context)

    @permission_required_method('write.wine_region', raise_exception=True)
    def delete(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        if data.regionImg:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, data.regionImg.url)[1:])
            except:
                pass
        data.delete()

        context['success'] = True
        context['message'] = '삭제되었습니다.'

        return JsonResponse(context, content_type='application/json')
        

class WineRegionEditView(LoginRequiredMixin, View):
    '''
    와인 지역 Edit
    김병주/2022.04.21
    '''
    login_url='system_manage:login'
    @permission_required_method('read.wine_region', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        context['data'] = data
        
        return render(request, 'wine_master/wine_region/wine_region_edit.html', context)
        
    @permission_required_method('write.wine_region', raise_exception=True)
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        pk=kwargs.get('pk')
        region = get_object_or_404(Region, pk=pk)
        name_kr = request.POST['name_kr']
        name_en = request.POST['name_en']
        image = request.FILES.get('image', None)
        description = request.POST['description']

        region.regionNameKr = name_kr
        region.regionNameEn = name_en
        region.regionDes = description
        if image:
            if region.regionImg:
                os.remove(os.path.join(settings.MEDIA_ROOT, region.regionImg.url)[1:])
            region.regionImg = image
            region.save()

        region.save()
        context['data_id'] = pk
        context['success'] = True
        context['message'] = '수정 되었습니다.'
        return JsonResponse(context, content_type='application/json')