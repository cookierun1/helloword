import imp
from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from shopping_mall.views.user_views.auth_views import HomeView, LoginView, RegisterView, ConfirmEmailView, activate

app_name = 'shopping_mall'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='shopping_mall:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),

]