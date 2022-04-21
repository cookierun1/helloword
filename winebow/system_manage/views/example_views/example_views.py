from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class ExampleTableView(LoginRequiredMixin, View):
    '''
    Sample Table
    김병주/2022.04.21
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, 'example/table_crud.html', context)

class ExampleTableCreateView(LoginRequiredMixin, View):
    '''
    Sample Create
    김병주/2022.04.21
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, 'example/table_crud_create.html', context)

class ExampleTableDetailView(LoginRequiredMixin, View):
    '''
    Sample Deatil
    김병주/2022.04.21
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['pk'] = kwargs.get('pk')
        return render(request, 'example/table_crud_detail.html', context)

class ExampleTableEditView(LoginRequiredMixin, View):
    '''
    Sample Edit
    김병주/2022.04.21
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, 'example/table_crud_edit.html', context)