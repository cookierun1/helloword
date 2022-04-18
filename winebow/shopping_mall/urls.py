import imp
from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from shopping_mall.views.user_views.auth_views import HomeView, LoginView, RegisterView, ConfirmEmailView, activate
from shopping_mall.views.user_views.password_reset_views import CustomPasswordResetConfirmView, UserPasswordResetView, \
    UserPasswordResetDoneView, UserPasswordResetCompleteView


app_name = 'shopping_mall'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='shopping_mall:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),

    path('password-reset/', UserPasswordResetView.as_view(), name="password_reset"),
    path('password-reset-done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]