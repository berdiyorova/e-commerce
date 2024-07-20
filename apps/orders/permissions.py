from rest_framework.permissions import BasePermission

from accounts.models import User


class IsOwnerOrEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user == request.user
            or request.user.role == User.Role.EMPLOYEE
        )
