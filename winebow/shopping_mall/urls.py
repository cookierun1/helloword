import imp
from django.urls.conf import path
from shopping_mall.views.user_views.auth_views import HomeView, LoginView

app_name = 'shopping_mall'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),

]