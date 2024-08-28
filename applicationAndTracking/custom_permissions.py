from rest_framework import permissions

class IsEmployerAndUpdateApplication(permissions.BasePermission):
    '''This will allow only employer to mark as accepeted or rejected or in review if they are creator of respective job and notification can be deleted by anyone.'''
    def has_permission(self, request, view):
        print(request.user.is_employer)
        if request.user.is_employer or request.method == 'DELETE':
            return True
        False
        
    def has_object_permission(self, request, view, obj):
        return obj.job.company==request.user
        