from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from system_manage.models import Wine, Grape, Region, Country, Winery
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from system_manage.utils import permission_required_method

class winemasterView(LoginRequiredMixin, View):
    '''
    와인 마스터 정보 관리
    박승원/2022.05.09
    '''
    login_url = 'system_manage:login'
    @permission_required_method('read.wine_master', redirect_url='system_manage:denied')
    def get(self,request: HttpRequest, *args, **kwargs):
        context={}
        wine=Wine.objects.all()
        context['wine']=wine

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