import imp
from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from system_manage.views.auth_views import HomeView, LoginView, PermissionDeniedView
from system_manage.views.user_manage_views import UserManageView
from system_manage.views.permission_manage_views import AccessPermissionView
from system_manage.views.access_manage_views import AccessManageView, GroupPermsListView
from system_manage.views.role_manage_views import RoleManageView


app_name = 'system_manage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='system_manage:login'), name='logout'),
    path('denied/', PermissionDeniedView.as_view(), name='denied'),

    path('user-manage/', UserManageView.as_view(), name='user_manage'),
    path('permission-manage/', AccessPermissionView.as_view(), name='permission_manage'),
    path('access-manage/', AccessManageView.as_view(), name='access_manage'),
    path('access-manage/permissions/', GroupPermsListView.as_view(), name='access_manage_permissions'),
    path('role-manage/', RoleManageView.as_view(), name='role_manage'),
]