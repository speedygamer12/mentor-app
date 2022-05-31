from rest_framework import permissions

# class IsAdmin(permissions.Permission):

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_staff)


class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
class IsActiveOwnerorReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:   
            return (obj.is_active and (obj.user == request.user)) or (request.user.is_staff)