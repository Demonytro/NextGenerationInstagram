from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.database.models import User, UserRole
from src.services.auth import auth_service


class RolesAccess:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")


access_admin = RolesAccess([UserRole.admin])
access_moderator = RolesAccess([UserRole.moderator])
access_admin_moderator = RolesAccess([UserRole.admin, UserRole.admin])
access_user = RolesAccess([UserRole.user])
access_user_admin = RolesAccess([UserRole.admin, UserRole.user])
access_all = RolesAccess([UserRole.admin, UserRole.moderator, UserRole.user])