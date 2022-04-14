import imp
from django.urls.conf import path
from shopping_mall.views import HomeView

app_name = 'shopping_mall'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]