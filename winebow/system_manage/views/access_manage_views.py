from django.db.models.query import QuerySet
from system_manage.utils import permission_required_method
from django.contrib.auth.mixins import LoginRequiredMixin
from system_manage.models import AccessPermission
from django.contrib.auth.models import Group
from system_manage.views.custom.paginated_listview import PaginatedListView
from system_manage.views.custom.searchable_listview import CriteriaNamePair, SearchableListView
from system_manage.views.role_manage_views import get_all_groups, get_group
from system_manage.views.permission_manage_views import filter_access_perms, get_access_perms
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import render


class GroupPermsListView(SearchableListView, PaginatedListView):
    # ListView
    model = AccessPermission
    context_object_name = 'access_permissions'
    template_name = 'access_manage.html'

    # PaginatedListView
    paginate_window_half = 2
    paginate_by = 10

    # SearchableListView
    IF_CRITERIA = [
        CriteriaNamePair("name" , "권한 이름"),
        CriteriaNamePair("url", "Access URL"),
    ]

    SEARCH_CRITERIA = {
        "name": "name",
        "url" : "codename"
    }
    
    def search_queryset(self, keyword, db_column) -> QuerySet:
        qset = AccessPermission.objects.filter(
            **{ 
                f'{db_column}__contains': keyword
            }
        )

        return qset

    def get_queryset(self) -> QuerySet:
        qset = super().get_queryset()
        group_id = self.request.GET.get('group_id', '')

        # Get all access permissions and check its possession.
        for perm in qset:
                perm.hasPerm = check_group_permission(group_id, perm.id)

        return filter_access_perms(qset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menucd'] = 'access_manage'
        context['menu_title'] = '그룹 권한 관리'

        try:
            group_id = self.request.GET.get('group_id', '')
            
            selected_group = get_group(group_id)
            if not selected_group:
                raise Exception('유효하지 않은 그룹입니다.')

            # Get all groups.
            groups = get_all_groups()

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])

        
        context['groups'] = groups
        context['selected_group'] = selected_group

        return context

    @permission_required_method('read.access_manage', raise_exception=True)
    def get(self, request: HttpRequest):
        """
        선택된 그룹의 권한 목록을 로드합니다.
        """

        return super().get(request)


class AccessManageView(LoginRequiredMixin, View):    
    login_url = 'system_manage:login'

    @permission_required_method('read.access_manage', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest):
        """
        그룹 권한 관리 초기 화면을 로드합니다.
        """

        context = {}
        context['menucd'] = 'access_manage'
        context['menu_title'] = '그룹 권한 관리'

        # Get all groups.
        groups = get_all_groups()

        context['groups'] = groups
        context['criteria_list'] = GroupPermsListView.IF_CRITERIA
        return render(request, 'access_manage.html', context)

    
    @permission_required_method('write.access_manage', raise_exception=True)
    def post(self, request: HttpRequest):
        """
        선택된 그룹의 권한 설정을 변경합니다.
        """

        context = {}
        context['menucd'] = 'access_manage'
        context['menu_title'] = '그룹 권한 관리'

        try:
            group_id = request.POST.get('group_id', '')
            permission_id = request.POST.get('permission_id', '')
            has_perm = str(request.POST.get('has_perm', '')).lower() == 'true'

            selected_group = get_group(group_id)
            if not selected_group:
                raise Exception('유효하지 않은 그룹입니다.')

            set_group_permission(group_id, permission_id, has_perm)
            
            # Get all access permissions and check its possession.
            perms = get_access_perms()
            for perm in perms:
                perm.hasPerm = check_group_permission(group_id, perm.id)

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])

        context['selected_group'] = selected_group
        context['access_permissions'] = perms
        return render(request, 'access_manage.html', context)


def set_group_permission(group_id, permission_id, has_perm):
    """
    그룹의 권한 소유여부를 변경합니다.
    """

    # TODO: 개별 함수로 분리하여 예외처리할 것.
    perm = AccessPermission.objects.get(id=permission_id)

    group = get_group(group_id)

    if (has_perm):
        group.permissions.add(perm)
    else:
        group.permissions.remove(perm)

def check_group_permission(group_id, permission_id):
    """
    그룹의 권한 소유여부를 체크합니다.
    """

    return Group.objects.filter(id=group_id, **{
        'permissions__id': permission_id
    }).exists()
