from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsProjectManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.manger == request.user or request.user.is_staff

class IsTashAssigneeOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user or obj.projet.manger == request.user or request.user.is_staff
    
class IsTashProjetManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.projet.manger == request.user or request.user.is_staff
    
    
class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser
