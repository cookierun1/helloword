from django.http import HttpRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from system_manage.models import Country
from django.http import HttpRequest, JsonResponse
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from system_manage.utils import permission_required_method


class winecountryView(LoginRequiredMixin, View):
    '''
    와인 나라 정보 관리
    박승원/2022.05.04
    '''
    login_url = 'system_manage:login'
    @permission_required_method('read.wine_country', redirect_url='system_manage:denied')
    def get(self,  request: HttpRequest, *args, **kwargs):
        context = {}
        paginate_by = '3'
        page = request.GET.get('page', '1')
        search_type = self.request.GET.get('search_type', '')
        search_keyword = self.request.GET.get('search_keyword', '')
        if search_keyword:
            context['search_type'] = search_type
            context['search_keyword'] = search_keyword
            if search_type == 'name_kr':
                country = Country.objects.filter(countryNameKr__icontains=search_keyword)
            elif search_type == 'name_en':
                country = Country.objects.filter(countryNameEn__icontains=search_keyword)
        else:
            country = Country.objects.all()

        paginator = Paginator(country, paginate_by)

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

        context['country'] = page_obj
        context['page_obj'] = page_obj

        return render(request, 'wine_master/wine_country/wine_country.html', context)


class winecountryCreateView( LoginRequiredMixin, View):
    '''
    와인 나라 Create
    박승원/2022.05.04
    '''
    login_url = 'system_manage:login'
    @permission_required_method('read.wine_country', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        return render(request, 'wine_master/wine_country/wine_country_create.html', context)

    @permission_required_method('write.wine_country', raise_exception=True)
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        name_kr = request.POST['name_kr']
        name_en = request.POST['name_en']
        image = request.FILES.get('image', None)
        description = request.POST['description']
        country = Country.objects.create(
            countryNameKr = name_kr,
            countryNameEn = name_en,
            countryDes = description
        )
        if image:
            country.countryImg = image
            country.save()

        context['success'] = True
        context['message'] = '등록 되었습니다.'
        return JsonResponse(context, content_type='application/json')


class WinecountryDetailView(LoginRequiredMixin, View):
    '''
    와인 국가 Deatil 및 삭제
    박승원/2022.05.04
    '''
    login_url = 'system_manage:login'
    @permission_required_method('read.wine_country', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Country, pk=kwargs.get('pk'))
        context['data'] = data
        return render(request, 'wine_master/wine_country/wine_country_detail.html', context)

    @permission_required_method('write.wine_country', raise_exception=True)
    def delete(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = get_object_or_404(Country, pk=kwargs.get('pk'))
        if data.countryImg:
            try:
                os.remove(data.countryImg.path)
            except:
                pass
        data.delete()

        context['success'] = True
        context['message'] = '삭제되었습니다.'

        return JsonResponse(context, content_type='application/json')

class WinecountryEditView(LoginRequiredMixin, View):
    '''
    와인 국가 Edit
    박승원/2022.05.04
    '''
    login_url = 'system_manage:login'
    @permission_required_method('read.wine_country', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        data=get_object_or_404(Country, pk=kwargs.get('pk'))
        context['data'] = data

        return render(request, 'wine_master/wine_country/wine_country_edit.html', context)

    @permission_required_method('write.wine_country', raise_exception=True)
    def post(self,  request: HttpRequest, *args, **kwargs):
        context={}
        pk=kwargs.get('pk')
        country = get_object_or_404(Country, pk=pk)
        name_kr = request.POST['name_kr']
        name_en = request.POST['name_en']
        image = request.FILES.get('image', None)
        description = request.POST['description']

        country.countryNameKr = name_kr
        country.countryNameEn = name_en
        country.countryDes = description

        if image:
            if country.countryImg:
                # 경로 수정
                try:
                    os.remove(country.countryImg.path)
                except:
                    pass
            country.countryImg = image
            country.save()

        country.save()
        context['data_id'] = pk
        context['success'] = True
        context['message'] = '수정 되었습니다.'
        return JsonResponse(context, content_type='application/json')


