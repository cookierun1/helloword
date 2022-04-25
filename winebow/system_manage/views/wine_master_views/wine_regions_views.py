import re
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
import os, json

from system_manage.utils import permission_required_method, get_epochtime_ms
from system_manage.models import Region

class WineRegionView(LoginRequiredMixin, View):
    '''
    와인 지역 정보 관리
    김병주/2022.04.22
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        region = Region.objects.all()
        context['region'] = region
        return render(request, 'wine_master/wine_region.html', context)


class WineRegionCreateView(LoginRequiredMixin, View):
    '''
    와인 지역 Create
    김병주/2022.04.25
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, 'wine_master/wine_region_create.html', context)

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
            file_ext = os.path.splitext(image.name)[1]
            file_name = str(region.id) + file_ext
            path = 'static/image/wine_master/region'
            fs = FileSystemStorage(location=path)
            fs.save(file_name, image)
            region.regionImg = path + f'/{file_name}'
            region.save()

        context['success'] = True
        context['message'] = '등록 되었습니다.'
        return JsonResponse(context, content_type='application/json')

class WineRegionDetailView(LoginRequiredMixin, View):
    '''
    와인 지역 Deatil 및 삭제
    김병주/2022.04.25
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        context['data'] = data
        return render(request, 'wine_master/wine_region_detail.html', context)
    
    def delete(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        if data.regionImg:
            os.remove(data.regionImg)
        data.delete()

        context['success'] = True
        context['message'] = '삭제되었습니다.'

        return JsonResponse(context, content_type='application/json')
        

class WineRegionEditView(LoginRequiredMixin, View):
    '''
    와인 지역 Edit
    김병주/2022.04.21
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Region, pk=kwargs.get('pk'))
        context['data'] = data
        
        return render(request, 'wine_master/wine_region_edit.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        region = get_object_or_404(Region, pk=kwargs.get('pk'))
        name_kr = request.POST['name_kr']
        name_en = request.POST['name_en']
        image = request.FILES.get('image', None)
        description = request.POST['description']

        region.regionNameKr = name_kr
        region.regionNameEn = name_en
        region.regionDes = description
        if image:
            if region.regionImg:
                os.remove(region.regionImg)
            file_ext = os.path.splitext(image.name)[1]
            file_name = str(region.id) + file_ext
            path = 'static/image/wine_master/region'
            fs = FileSystemStorage(location=path)
            fs.save(file_name, image)
            region.regionImg = path + f'/{file_name}'

        region.save()

        context['success'] = True
        context['message'] = '등록 되었습니다.'
        return JsonResponse(context, content_type='application/json')