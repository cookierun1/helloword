from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from system_manage.views.system_manage_views.auth_views import HomeView, LoginView, PermissionDeniedView
from system_manage.views.system_manage_views.user_manage_views import UserManageView
from system_manage.views.system_manage_views.permission_manage_views import AccessPermissionView
from system_manage.views.system_manage_views.access_manage_views import AccessManageView, GroupPermsListView
from system_manage.views.system_manage_views.role_manage_views import RoleManageView

from system_manage.views.wine_master_views.wine_regions_views import WineRegionView, WineRegionCreateView, WineRegionDetailView, WineRegionEditView
from system_manage.views.example_views.jqGrid_sample_views import GridSampleView, SampleView
from system_manage.views.example_views.editor_sample_views import EditorSampleView, EditorSampleCreateView, EditorSampleDetailView, EditorSampleEditView

app_name = 'system_manage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='system_manage:login'), name='logout'),
    path('denied/', PermissionDeniedView.as_view(), name='denied'),

    # 회원, 권한 접근 관리
    path('user-manage/', UserManageView.as_view(), name='user_manage'),
    path('permission-manage/', AccessPermissionView.as_view(), name='permission_manage'),
    path('access-manage/', AccessManageView.as_view(), name='access_manage'),
    path('access-manage/permissions/', GroupPermsListView.as_view(), name='access_manage_permissions'),
    path('role-manage/', RoleManageView.as_view(), name='role_manage'),

    # jqGrid Sample
    path('jqgrid-sample/', SampleView.as_view(), name='jqgrid_sample'),
    path('grid_sample', GridSampleView.as_view(),name='grid_sample'),

    # Editor Sample
    path('editor-sample/', EditorSampleView.as_view(), name='editor_sample'),
    path('editor-sample-create/', EditorSampleCreateView.as_view(), name='editor_sample_create'),
    path('editor-sample-detail/<int:pk>', EditorSampleDetailView.as_view(), name='editor_sample_detail'),
    path('editor-sample-edit/<int:pk>', EditorSampleEditView.as_view(), name='editor_sample_edit'),




    # 와인 지역
    path('wine-region/', WineRegionView.as_view(), name='wine_region'),
    path('wine-region-create/', WineRegionCreateView.as_view(), name='wine_region_create'),
    path('wine-region-detail/<int:pk>', WineRegionDetailView.as_view(), name='wine_region_detail'),
    path('wine-region-edit/<int:pk>', WineRegionEditView.as_view(), name='wine_region_edit'),
    
]