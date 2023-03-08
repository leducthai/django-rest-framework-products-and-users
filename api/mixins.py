from rest_framework import permissions
from .permission import isstaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser , isstaffEditorPermission]

class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False

    def get_queryset(self , *args , **kwargs):
        lookup_data = {}
        user = self.request.user
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args , **kwargs)
        qs2 = qs.filter(published=True)

        if user.is_staff and self.allow_staff_view:
            return qs
        

        return (qs.filter(**lookup_data) | qs2).distinct()