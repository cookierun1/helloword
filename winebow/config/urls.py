from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include('shopping_mall.urls')),
    path('system-manage/', include('system_manage.urls')),
    path('pos-system/', include('pos_system.urls')),
]
