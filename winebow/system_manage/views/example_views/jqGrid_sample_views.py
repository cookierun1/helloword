from django.views.generic import View, TemplateView

class GridSampleView(TemplateView):
    """
    jqGrid 페이지 로드.
    김병주/2022.04.26
    """
    template_name = 'example/jqGrid_sample.html'