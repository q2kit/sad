from django.http import HttpResponseForbidden, Http404


def superadmin_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_superadmin:
                return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Superadmin required")
    return wrapper


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user and (request.user.is_admin or request.user.is_superadmin):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Admin required")
    return wrapper


def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user and (request.user.is_staff or request.user.is_admin or request.user.is_superadmin):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Staff required")
    return wrapper


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Login required")
    return wrapper