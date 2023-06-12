from fastapi import HTTPException, status
from functools import wraps

def has_role(role):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapper(current_user):
            if current_user.role not in role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
            return await view_func(current_user)
        return wrapper
    return decorator

