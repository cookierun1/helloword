from django.views.generic import View, TemplateView
from django.http.request import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from system_manage.models import Grape
from django.core import serializers
from django_summernote.widgets import SummernoteWidget

class EditorSampleView(TemplateView):
    """
    Editor 페이지 로드.
    김병주/2022.04.29
    """
    template_name = 'example/editor_sample.html'