from rest_framework import permissions

class IsEmployerUpdateOwnJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.company==request.user:
            return True
        return False
