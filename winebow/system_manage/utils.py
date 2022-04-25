from django.contrib.auth.decorators import permission_required
import datetime

def permission_required_method(perm, redirect_url=None, raise_exception=False):
    """
    Decorator for a http method of class view that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def decorator(view_method):
        def ignore_self(self, request, *args, **kwargs):
            def _view_func(request, *args, **kwargs):
                return view_method(self, request, *args, **kwargs)

            _dec = permission_required(perm, redirect_url, raise_exception)
            _wrapped_view = _dec(_view_func)

            return _wrapped_view(request, *args, **kwargs)

        return ignore_self

    return decorator


def get_epochtime_ms():
    '''
    밀리 초 단위로 현재 UTC 시간 얻는 함수
    김병주 (2022/04/25)
    '''
    return round(datetime.utcnow().timestamp() * 1000)