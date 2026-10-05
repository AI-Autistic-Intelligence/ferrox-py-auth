from functools import wraps
from typing import List, Any, Callable
from fastapi import Request
from ferrox_py.core.errors import FerroxError

def require_roles(*roles: str) -> Callable[[Any], Any]:
    """
    RBAC Decorator.
    Extracts the user 'roles' claim from the JWT (attached to request.state.user)
    and validates it against the required roles.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            user_data = getattr(request.state, "user", None)
            if not user_data:
                raise FerroxError("Unauthorized - No JWT token found", 401)
                
            user_roles = user_data.get("roles", [])
            
            if not any(role in user_roles for role in roles):
                raise FerroxError(f"Forbidden - Requires one of roles: {roles}", 403)
                
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
