from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Core bouncer logic: Checks if the logged-in user's session role 
    matches the allowed clearance levels for a specific view.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Grab the current logged-in user's role from session memory
            user_role = request.session.get("logged_in_user_role")
            
            # 2. If they aren't logged in, or their role isn't on the guest list: ACCESS DENIED
            if not user_role or user_role not in allowed_roles:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You do not have the required security clearance to access this zone.</p>"
                )
            
            # 3. Otherwise, let them through to the view!
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# 🌟 Explicit decorators for our 3 target zones:
def customer_required(view_func):
    return role_required(allowed_roles=['STANDARD'])(view_func)

def agent_required(view_func):
    return role_required(allowed_roles=['SUPERVISOR'])(view_func)

def admin_required(view_func):
    return role_required(allowed_roles=['ADMIN'])(view_func)