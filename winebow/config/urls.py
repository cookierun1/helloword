from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('accounts/', include('allauth.urls')),
    
    #app
    path('', include('shopping_mall.urls')),
    path('system-manage/', include('system_manage.urls')),
    path('shop-manage/', include('shop_manage.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
