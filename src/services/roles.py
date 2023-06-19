# from typing import List
#
# from fastapi import Depends, HTTPException, status, Request
#
# from src.database.models import User, UserRole
# from src.services.auth import auth_service
#
#
# class RoleChecker:
#     def __init__(self, allowed_roles: List[UserRole]):
#         self.allowed_roles = allowed_roles
#
#     async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
#         if current_user.role not in self.allowed_roles:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")


from typing import List

from fastapi import Request, Depends, HTTPException, status
from cloudinary.provisioning import Role                       #, UserRole   #  ----------, Role

from src.database.models import User, UserRole   #  ----------, Role
from src.services.auth import auth_service


class RolesAccess:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")