from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or request.user.has_perm("orders.can_change_status")
        )
