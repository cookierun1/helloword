from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField (
        label='',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'id': 'email',
                'autocomplete': 'email', 
                'class': 'form-control', 
                'placeholder': 'Email'
            })
    )
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'class': 'form-control', 
                'placeholder': 'New Password'
            }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control', 
            'placeholder': 'Confirm Password'
        }),
    )

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('shopping_mall:password_reset_complete')
    template_name = 'user/password_reset_confirm.html'


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'user/password_reset_email.html'
    subject_template_name = 'user/password_reset_subject.txt'
    template_name = 'user/password_reset.html'
    success_url = reverse_lazy('shopping_mall:password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'user/password_reset_done_fail.html')
            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'

class UserPasswordResetCompleteView(PasswordResetDoneView):
    template_name = 'user/password_reset_complete.html'