from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


ROLE_DASHBOARD_URLS = {
    "admin": "role_dashboard_admin",
    "doctor": "role_dashboard_doctor",
    "nurse": "role_dashboard_nurse",
    "care_assistant": "role_dashboard_care_assistant",
    "family": "family_portal",
}


def dashboard_url_for_user(user):
    """Return the first page a signed-in user should see for their role."""
    return ROLE_DASHBOARD_URLS.get(getattr(user, "role", ""), "dashboard")


def role_required(*allowed_roles):
    """Guard role-specific pages so staff cannot open another role interface."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, "Access denied for this role dashboard.")
                return redirect(dashboard_url_for_user(request.user))
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
