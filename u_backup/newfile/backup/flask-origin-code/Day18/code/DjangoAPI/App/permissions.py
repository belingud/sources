from rest_framework.permissions import BasePermission

from App.models import User


class LoginPermission(BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.user, User)

    def has_object_permission(self, request, view, obj):
        # 超管  或着  拥有者
        return request.user.is_super or request.user.u_animals.filter(pk=obj.id).exists()


class SearchPermission(BasePermission):
    # confirm login when clients search for information of users and animals
    def has_permission(self, request, view):
        return isinstance(request.user, User)

