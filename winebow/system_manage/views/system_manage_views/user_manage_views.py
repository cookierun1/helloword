
from system_manage.utils import permission_required_method
from django.contrib.auth.models import Group, User
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from system_manage.views.custom.paginated_listview import PaginatedListView
from system_manage.views.custom.searchable_listview import CriteriaNamePair, SearchableListView
from system_manage.views.system_manage_views.role_manage_views import get_all_groups
from django.core.paginator import Paginator

class UserManageView(SearchableListView, PaginatedListView):
    model = User
    paginate_by = 10
    paginate_window_half = 2
    context_object_name = 'users'
    template_name = 'system_manage/user_manage.html'

    IF_CRITERIA = [
        CriteriaNamePair('user_id', '사용자 ID'),
        CriteriaNamePair('name', '사용자 이름'),
        CriteriaNamePair('email', '이메일'),
    ]

    SEARCH_CRITERIA = { 
        'user_id': 'username',
        'name': 'last_name',
        'email': 'email',
    }

    def search_queryset(self, keyword, db_column):
        return search_users(keyword, db_column)
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        # Get all groups.
        groups = get_all_groups()
        context['groups'] = groups

        return context

    @permission_required_method('read.user_manage', redirect_url='system_manage:denied')
    def get(self, request: HttpRequest):
        """
        사용자를 조회합니다.
        """
        
        return super().get(request)
    
    @permission_required_method('write.user_manage', raise_exception=True)
    def post(self, request: HttpRequest):
        """
        사용자를 생성합니다.
        """
        
        context = {}

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        groups = request.POST.get('groups', None)
        first_name = request.POST.get('first_name', None) 
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        
        # Create new user.
        try:
            create_user(
                username=username,
                email=email,
                password=password,
                groups=groups,
                first_name=first_name,
                last_name=last_name,
            )

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])


        # Get all users.
        users = get_all_users()

        # Get all groups.
        groups = get_all_groups()

        context['users'] = users
        context['groups'] = groups

        return render(request, 'system_manage/user_manage.html', context)

    @permission_required_method('write.user_manage', raise_exception=True)
    def put(self, request: HttpRequest):
        """
        사용자를 수정합니다.
        """

        context = {}

        request.PUT = QueryDict(request.body)

        user_id = request.PUT.get('id', None)
        groups = request.PUT.get('groups', None)
        first_name = request.PUT.get('first_name', None)
        last_name = request.PUT.get('last_name', None)
        email = request.PUT.get('email', None)
        is_active = request.PUT.get('is_active', None)

        # Update user.
        try:
            update_user(
                user_id,
                groups=groups,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=is_active
            )

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])


        # Get all users.
        users = get_all_users()

        # Get all groups.
        groups = get_all_groups()

        context['users'] = users
        context['groups'] = groups

        return render(request, 'system_manage/user_manage.html', context)


    @permission_required_method('write.user_manage', raise_exception=True)
    def delete(self, request: HttpRequest):
        """
        시용자를 삭제합니다.
        """

        context = {}

        request.DELETE = QueryDict(request.body)

        user_id = request.DELETE.get('id', None)
        
        # Delete user.
        try:
            is_deleted = delete_user(user_id)
            if not is_deleted:
                raise Exception('삭제 불가능한 사용자입니다.')

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e.args[0])


        # Get all users.
        users = get_all_users()

        # Get all groups.
        groups = get_all_groups()

        context['users'] = users
        context['groups'] = groups

        return render(request, 'system_manage/user_manage.html', context)

def search_users(keyword: str, criteria: str, *fields):
    return get_all_users(*fields).filter(
            **{ 
                f'{criteria}__contains': keyword
            }
        )

def get_all_users(*fields):
    """
    Get all users with selected fields.
    """

    # Default 
    if not fields:
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'groups'
        )

    return User.objects.values(*fields)

def create_user(username, email, password, **extra_fields):
    """
    Create new user. `username` and `password` are required.
    """

    from django.conf import settings
    DEFAULT_PASSWORD = settings.DEFAULT_PASSWORD
    DEFAULT_GROUP = settings.DEFAULT_GROUP

    # Validate parameters.
    password = password if password else DEFAULT_PASSWORD

    if not Group.objects.filter(id=extra_fields['groups']).exists():
        default_group, _ = Group.objects.get_or_create(name=DEFAULT_GROUP)
        extra_fields['groups'] = default_group.id

    # Remove `groups` from extra_fields.
    groups = extra_fields['groups']
    del extra_fields['groups']
    user_created = User.objects.create_user(username, email, password, **extra_fields)
    user_created.groups.add(groups)

    return user_created

def update_user(user_id, **fields_to_update):
    user_to_update:User = User.objects.get(id=user_id)

    # Update user.
    user_to_update.first_name = fields_to_update['first_name']
    user_to_update.last_name = fields_to_update['last_name']
    user_to_update.email = fields_to_update['email']
    user_to_update.is_active = str(fields_to_update['is_active']).lower() == 'true'
    user_to_update.save()

    # Update user's group.
    user_to_update.groups.clear()
    user_to_update.groups.add(fields_to_update['groups'])

def delete_user(user_id):
    _, res_dict = User.objects.filter(id=user_id).delete()
    return res_dict[User._meta.label] == 1