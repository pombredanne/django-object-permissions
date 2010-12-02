from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission

from perms.models import UserObjectPermission, GroupObjectPermission

class ObjectPermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    
    def authenticate(self, username, password):
        return None
    
    def has_module_perms(self, user_obj, app_label):
        #TODO: actually introspect for permissions?
        # Actual permissions are checked anyways, returning false is just a way
        # to save time if you're sure they don't have permissions.
        return True

    def has_perm(self, user_obj, perm, obj=None):
        # "If `obj` is None, this should return True if the given request has
        #  permission to [act on] *any* object of the given type."
       
        if obj is not None:
            ct = ContentType.objects.get_for_model(obj)
        else:
            try:
                perm_obj = Permission.objects.get(codename = perm.split('.')[-1])
                ct = perm_obj.content_type
            except ObjectDoesNotExist:
                return False

        try:
            perm = perm.split('.')[-1].split("_")[0]
        except IndexError:
            return False

        user_perms = UserObjectPermission.objects.filter(content_type=ct, 
                user=user_obj)
        group_perms = GroupObjectPermission.objects.filter(content_type=ct,
                group__in=user_obj.groups.all())
        
        if obj is not None:
            user_perms = user_perms.filter(object_id = obj.id)
            group_perms = group_perms.filter(object_id = obj.id)
            
        kwargs = {'can_%s' % perm: True}
        try:
            return bool(group_perms.filter(**kwargs) or user_perms.filter(**kwargs))
        except FieldError:
            return False

