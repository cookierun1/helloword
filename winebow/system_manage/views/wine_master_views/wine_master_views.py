from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from system_manage.models import Wine, Grape, Region, Country, Winery
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from system_manage.utils import permission_required_method
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


class winemasterView(LoginRequiredMixin, View):
        '''
        와인 마스터 정보 관리
        박승원/2022.05.10
        '''
        login_url = 'system_manage:login'
        @permission_required_method('read.wine_master', redirect_url='system_manage:denied')
        def get(self,request: HttpRequest, *args, **kwargs):
            context = {}
            paginate_by = '3'
            page = request.GET.get('page', '1')
            search_type = self.request.GET.get('search_type', '')
            search_keyword = self.request.GET.get('search_keyword', '')
            if search_keyword:
                context['search_type'] = search_type
                context['search_keyword'] = search_keyword
                if search_type == 'name_kr':
                    wine = Wine.objects.filter(wineNameKr__icontains=search_keyword)
                elif search_type == 'name_en':
                    wine = Wine.objects.filter(wineNameEn__icontains=search_keyword)
            else:
                wine = Wine.objects.all()

            paginator = Paginator(wine, paginate_by)

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

            context['wine'] = page_obj
            context['page_obj'] = page_obj

            return render(request, 'wine_master/wine/wine_master.html', context)

class winemasterCreateView(LoginRequiredMixin, View):
        '''
        와인 마스터 Create
        박승원/2022.05.09
        '''
        login_url = 'system_manage:login'
        @permission_required_method('read.wine_master', redirect_url='system_manage:denied')
        def get(self, request: HttpRequest, *args, **kwargs):
            context={}
            country = Country.objects.all()
            context['country'] = country
            region = Region.objects.all()
            context['region'] = region
            grape = Grape.objects.all()
            context['grape']=grape
            winery=Winery.objects.all()
            context['winery'] = winery
            return render(request, 'wine_master/wine/wine_master_create.html', context)

        @permission_required_method('write.wine_master', raise_exception=True)
        def post(self,request: HttpRequest, *args, **kwargs):

            context={}

            wine_num= request.POST['wine_num']
            print(wine_num)
            name_kr = request.POST['name_kr']
            name_en = request.POST['name_en']
            description = request.POST['description']
            image = request.FILES.get('image', None)
            print(image)
            country = request.POST.get('selectBox')
            print(country)
            region= request.POST.get('selectBox1')
            print(region)
            grape= request.POST.get('selectBox2')
            print(grape)
            winery= request.POST.get('selectBox3')
            print(winery)


            wine = Wine.objects.create(
                wineNum=wine_num,
                wineNameEn=name_en,
                wineNameKr=name_kr,
                wineDes=description,
                wma_country=Country.objects.get(id=country),
                wma_region=Region.objects.get(id=region),
                wma_grape=Grape.objects.get(id=grape),
                wma_winery=Winery.objects.get(id=winery)
            )
            if image:
                wine.wineImg = image
                wine.save()

            context['success'] = True
            context['message'] = '등록 되었습니다.'
            return JsonResponse(context, content_type='application/json')

class WinemasterDetailView(LoginRequiredMixin, View):
        '''
        와인 마스터 Deatil 및 삭제
        박승원/2022.05.10
        '''
        login_url = 'system_manage:login'
        @permission_required_method('read.wine_master', redirect_url='system_manage:denied')
        def get(self, request: HttpRequest, *args, **kwargs):
            context={}
            data = get_object_or_404(Wine, pk=kwargs.get('pk'))
            context['data'] = data
            return render(request, 'wine_master/wine/wine_master_detail.html', context)

        @permission_required_method('write.wine_master', raise_exception=True)
        def delete(self, request: HttpRequest, *args, **kwargs ):
            context = {}
            data = get_object_or_404(Wine, pk=kwargs.get('pk'))
            if data.wineImg:
                try:
                    os.remove(data.wineImg.path)
                except:
                    pass
            data.delete()

            context['success'] = True
            context['message'] = '삭제되었습니다.'

            return JsonResponse(context, content_type='application/json')


class WinemasterEditView(LoginRequiredMixin, View):
        '''
        와인 국가 Edit
        박승원/2022.05.10
        '''
        login_url = 'system_manage:login'
        @permission_required_method('read.wine_master', redirect_url='system_manage:denied')
        def get(self, request: HttpRequest, *args, **kwargs):
            context={}
            data = get_object_or_404(Wine, pk=kwargs.get('pk'))
            context['data'] = data

            country = Country.objects.all()
            context['country'] = country
            region = Region.objects.all()
            context['region'] = region
            grape = Grape.objects.all()
            context['grape'] = grape
            winery = Winery.objects.all()
            context['winery'] = winery

            return render(request, 'wine_master/wine/wine_master_edit.html', context)

        @permission_required_method('write.wine_master', raise_exception=True)
        def post(self, request: HttpRequest, *args, **kwargs):
            context={}
            pk=kwargs.get('pk')
            wine = get_object_or_404(Wine, pk=pk)
            wine_num=request.POST['wine_num']
            print(wine_num)
            name_kr = request.POST['name_kr']
            name_en = request.POST['name_en']
            image = request.FILES.get('image', None)
            description = request.POST['description']

            country = request.POST.get('selectBox')
            print(country)
            region= request.POST.get('selectBox1')
            print(region)
            grape= request.POST.get('selectBox2')
            print(grape)
            winery= request.POST.get('selectBox3')
            print(winery)

            wine.wineNum=wine_num
            wine.wineNameKr=name_kr
            wine.wineNameEn=name_en
            wine.wineDes=description
            if country:
                try:
                    wine.wma_country = Country.objects.get(id=country)
                except:
                    pass
            if region:
                try:
                    wine.wma_region = Region.objects.get(id=region)
                except:
                    pass
            if grape:
                try:
                  wine.wma_grape = Grape.objects.get(id=grape)
                except:
                    pass
            if winery:
                try:
                    wine.wma_winery= Winery.objects.get(id=winery)
                except:
                    pass

            if image:
                if wine.wineImg:
                    # 경로 수정
                    try:
                        os.remove(wine.wineImg.path)
                    except:
                        pass
                wine.wineImg = image
            wine.save()

            context['data_id'] = pk
            context['success'] = True
            context['message'] = '수정 되었습니다.'
            return JsonResponse(context, content_type='application/json')


