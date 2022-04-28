from django.views.generic import View, TemplateView
from django.http.request import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from system_manage.models import Grape
from django.core import serializers

class SampleView(TemplateView):
    """
    jqGrid 페이지 로드.
    김병주/2022.04.26
    """
    template_name = 'example/jqGrid_sample.html'


class GridSampleView(LoginRequiredMixin, View):

    JQGRID_DEFAULT_EMPTY = '_empty'


    def get(self, request: HttpRequest, *args, **kwargs):

        items = list(Grape.objects.all().values())
        return JsonResponse(data=items, safe=False)
    

    def post(self, request: HttpRequest, *args, **kwargs):
        item_id = request.POST.get('id', None)
        item_id = item_id if item_id != self.JQGRID_DEFAULT_EMPTY else None
        grapeNameEn  = request.POST.get('grapeNameEn', None)
        grapeNameKr  = request.POST.get('grapeNameKr', None)
        grapeDes  = request.POST.get('grapeDes', None)
          
        if item_id is None:
            # Create new item.
            Grape.objects.create(
                grapeNameEn =  grapeNameEn,
                grapeNameKr =  grapeNameKr,
                grapeDes =  grapeDes,

            )
            return JsonResponse(data={ 'success': True, 'newID':item_id })

        return JsonResponse(data={ 'success': False })

    def put(self, request: HttpRequest):
        request.PUT = QueryDict(request.body)
        item_id = request.PUT.get('id', None)
        item_id = item_id if item_id != self.JQGRID_DEFAULT_EMPTY else None
        grapeNameEn  = request.PUT.get('grapeNameEn', None)
        grapeNameKr  = request.PUT.get('grapeNameKr', None)
        grapeDes  = request.PUT.get('grapeDes', None)
        
        if item_id is not None:
            #  Update existing item.
            Grape.objects.filter(id=item_id).update(
                grapeNameEn =  grapeNameEn,
                grapeNameKr =  grapeNameKr,
                grapeDes =  grapeDes,
            )
            return JsonResponse(data={ 'success': True })

        return JsonResponse(data={ 'success': False })
    
    def delete(self, request: HttpRequest):
        request.DELETE = QueryDict(request.body)
        
        item_id = request.DELETE.get('id', None)
        if item_id is not None:
            Grape.delete(Grape.objects.get(id=item_id))
            return JsonResponse(data={ 'success': True })

        return JsonResponse(data={ 'success': False })
    