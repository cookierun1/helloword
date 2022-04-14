from system_manage.utils import permission_required_method
from django.contrib.auth.models import Group, User
from django.http.request import HttpRequest, QueryDict
from django.http.response import JsonResponse
from django.views.generic import View

class RoleManageView(View):
    @permission_required_method('write.role_manage', raise_exception=True)
    def post(self, request: HttpRequest):
        """
        그룹을 생성합니다.
        """
        context = {}
        context['menucd'] = 'role_manage'
        context['menu_title'] = '역할 관리'

        try:
            group_name = request.POST.get('group_name', '')

            is_valid = check_group_name(group_name)
            if not is_valid:
                raise Exception('생성 불가능한 그룹 이름입니다.')

            create_group(group_name)

        except Exception as e:
            print(e)
            context['success'] = False
            context['message'] = e.args[0]
            return JsonResponse(context, content_type='application/json')


        context['success'] = True
        return JsonResponse(context, content_type='application/json')

    @permission_required_method('write.role_manage', raise_exception=True)
    def delete(self, request: HttpRequest):
        """
        그룹을 삭제합니다.
        """
        context = {}
        context['menucd'] = 'role_manage'
        context['menu_title'] = '역할 관리'

        try:
            request.DELETE = QueryDict(request.body)
            group_id = request.DELETE.get('group_id', '')

            # group = get_group(group_id)
            # if not group:
            #     raise Exception('삭제 불가능한 그룹 이름입니다.')

            can_be_deleted = check_group_deletion(group_id)
            if not can_be_deleted:
                raise Exception('해당 그룹에 사용자가 있어 삭제가 불가능합니다.')
                 
            is_deleted = delete_group(group_id)
            if not is_deleted:
                raise Exception('그룹을 삭제하는 중에 오류가 발생했습니다.')

        except Exception as e:
            print(e)
            context['success'] = False
            context['message'] = e.args[0]
            return JsonResponse(context, content_type='application/json')

        
        context['success'] = True
        return JsonResponse(context, content_type='application/json')


def delete_group(gid):
    _, res_dict = Group.objects.filter(id=gid).delete()
    return res_dict[Group._meta.label] == 1

def check_group_deletion(gid):
    return not User.objects.filter(
        **{
            'groups__id': gid
        }
    ).exists()

def get_group(gid):
    grp_qset = Group.objects.filter(id=gid)
    
    grp = None
    if grp_qset.exists():
        grp = grp_qset.first()
        
    return grp 

def get_all_groups():
    return Group.objects.all()


def check_group_name(group_name):
    """
    그룹이름의 중복 여부를 체크합니다.
    """
    grp_qset = Group.objects.filter(
        name=group_name
    )

    return not grp_qset.exists()

def create_group(group_name):
    """
    그룹을 생성합니다.
    """
    created = Group.objects.create(
        name=group_name
    )

    return created