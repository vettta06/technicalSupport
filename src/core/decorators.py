from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """Декоратор, разрешающий доступ только
    пользоватлям с определённой ролью.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if (hasattr(request.user, 'role') and
                request.user.role in allowed_roles):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "У вас нет доступа к этой странице.")
                return redirect('dashboard') 
        return _wrapped_view
    return decorator
