from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from perms.models import *

class ObjectPermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False

        ct = ContentType.objects.get_for_model(obj)

        try:
            perm = perm.split('.')[-1].split("_")[0]
        except IndexError:
            return False

        user_perms = UserObjectPermission.objects.filter(content_type=ct,
                object_id=obj.id, user=user_obj)
        group_perms = GroupObjectPermission.objects.filter(content_type=ct,
                object_id=obj.id, group__in=user_obj.groups.all())

        has_user_perms = any(map(lambda k: getattr(k, 'can_%s' % perm), user_perms))
        has_group_perms = any(map(lambda k: getattr(k, 'can_%s' % perm), group_perms))

        return has_group_perms or has_user_perms

