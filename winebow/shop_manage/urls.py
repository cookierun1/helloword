from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from shop_manage.views.shop_manage_views.auth_views import HomeView, LoginView, PermissionDeniedView
app_name = 'shop_manage'
urlpatterns = [
    path('<int:pk>/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:pk>/logout/', LogoutView.as_view(next_page='shop_manage:login'), name='logout'),
    path('denied/', PermissionDeniedView.as_view(), name='denied'),
]