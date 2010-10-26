from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

class ObjectPermission(models.Model):
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    class Meta():
        abstract = True

class UserObjectPermission(ObjectPermission):
    user = models.ForeignKey(User, related_name = "object_permissions")

class GroupObjectPermission(ObjectPermission):
    group = models.ForeignKey(Group, related_name = "object_permissions")

