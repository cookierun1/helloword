from django import forms
from system_manage.models import Board
from django_summernote.widgets import SummernoteWidget


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'id' : 'title',
                'class': "form-control",
            }),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }