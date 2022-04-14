from django.db.models.query import QuerySet
from system_manage.utils import permission_required_method
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponseBadRequest
from django.views.generic import View
from system_manage.models import AccessPermission
from django.shortcuts import render
from django.db.models import F

from system_manage.views.custom.paginated_listview import PaginatedListView
from system_manage.views.custom.searchable_listview import CriteriaNamePair, SearchableListView

class AccessPermissionView(LoginRequiredMixin, SearchableListView, PaginatedListView):
    # LoginRequiredMixin
    login_url = 'system_manage:login'

    # ListView
    model = AccessPermission
    context_object_name = 'access_permissions'
    template_name = 'permission_manage.html'

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

        return filter_access_perms(qset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    @permission_required_method('read.permission_manage', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest):
        """
        권한을 조회합니다.
        """

        return super().get(request)

    @permission_required_method('write.permission_manage', raise_exception=True)
    def post(self, request: HttpRequest):
        """
        권한을 생성힙니다.
        """
        
        context = {}

        try:
            perm_name = request.POST.get('name', None)
            perm_url = request.POST.get('codename', None)

            # Create access(read or write) permission.
            _, is_read_created = get_or_create_read_perm(perm_name, perm_url)
            _, is_write_created = get_or_create_write_perm(perm_name, perm_url)
            if not (is_read_created or is_write_created):
                raise Exception('이미 존재하는 메뉴 입니다.')

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])

        # Get all access permissions.
        perms = get_access_perms()

        context['access_permissions'] = perms
        return render(request, 'permission_manage.html', context)
        
    
    @permission_required_method('write.permission_manage', raise_exception=True)
    def put(self, request: HttpRequest):
        """
        권한을 수정합니다.
        """
        
        context = {}

        try:
            request.PUT = QueryDict(request.body)
            perm_id = request.PUT.get('id', None)
            perm_name = request.PUT.get('name', None)
            perm_url = request.PUT.get('codename', None)
            
            # Update access permission.
            is_updated = update_access_perm(perm_id, perm_name, perm_url)
            if not is_updated:
                raise Exception('해당 값으로 수정할 수 없습니다.')

        except Exception as e:
            return HttpResponseBadRequest(e.args[0])

        # Get all access permissions.
        perms = get_access_perms()

        context['access_permissions'] = perms
        return render(request, 'permission_manage.html', context)
        
    
    @permission_required_method('write.permission_manage', raise_exception=True)
    def delete(self, request: HttpRequest):
        """
        권한을 삭제합니다.
        """
        
        context = {}

        try:
            request.DELETE = QueryDict(request.body)
            perm_id = request.DELETE.get('id', None)
            
            # Delete access permission.
            is_deleted = delete_access_perm(perm_id)
            if not is_deleted:
                raise Exception('삭제 불가능한 항목입니다.')

        except Exception as e:
            return HttpResponseBadRequest(e.args[0])

        # Get all access permissions.
        perms = get_access_perms()

        context['access_permissions'] = perms
        return render(request, 'permission_manage.html', context)
        

def delete_access_perm(id):
    _, res_dict = AccessPermission.objects.filter(id=id).delete()
    return res_dict[AccessPermission._meta.label] == 1

def update_access_perm(id, name, perm_url):
    updated_rows = AccessPermission.objects.filter(id=id).update(
        name=name,
        codename=make_codename(perm_url)
    )
    
    return updated_rows == 1

def get_access_perms():
    qset = AccessPermission.objects.all()
    return filter_access_perms(qset)

def filter_access_perms(qset: QuerySet):
    for perm in qset:
        # Convert codename to url.
        perm.codename = normalize_url(perm.codename)

        # Convert content type.
        if perm.content_type_id == AccessPermission.PERMISSION_TYPE.READ.id:
            perm.content_type_id = "Read"
        elif perm.content_type_id == AccessPermission.PERMISSION_TYPE.WRITE.id:
            perm.content_type_id = "Write"

    return qset 

def get_or_create_read_perm(name, perm_url):
    perm_url = normalize_url(perm_url)
    
    return AccessPermission.objects.get_or_create(
        name=name,
        codename=make_codename(perm_url),
        content_type=AccessPermission.PERMISSION_TYPE.READ,
    )

def get_or_create_write_perm(name, perm_url):
    perm_url = normalize_url(perm_url)

    return AccessPermission.objects.get_or_create(
        name=name,
        codename=make_codename(perm_url),
        content_type=AccessPermission.PERMISSION_TYPE.WRITE,
    )

def normalize_url(perm_url: str):
    # if not perm_url.startswith('/'):
    #     perm_url = '/' + perm_url
    return perm_url.lower()

def make_codename(perm_url: str):
    perm_url = normalize_url(perm_url)

    return str(perm_url)\
        # .replace('-', '_')\
        # .replace('/', '_')\
        # .replace('_', '', 1)
