from fastapi import HTTPException, status
from functools import wraps
from src.database.models import Image
def has_role(role):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapper(current_user, image_id=None, db=None):
            if not image_id:
                if current_user.role not in role:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
            else:
                image_user_id = db.query(Image).filter(Image.id == image_id).first().user_id
                if current_user.role not in role and image_user_id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges for current user")
            return await view_func(current_user)
        return wrapper
    return decorator


