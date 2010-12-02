from django.contrib import admin
from django.contrib import messages
from django.contrib.contenttypes.generic import GenericTabularInline
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import *
from perms.models import *

class UserObjectPermissionInline(GenericTabularInline):
    model = UserObjectPermission

class GroupObjectPermissionInline(GenericTabularInline):
    model = GroupObjectPermission

class ObjectPermissionMixin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):

        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + \
                opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):

        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + \
                opts.get_delete_permission(), obj)
        
    def change_view(self, request, *args, **kwargs):
        try:
            return super(ObjectPermissionMixin, self).change_view(request, *args, **kwargs)
        except PermissionDenied, e:
            ct = ContentType.objects.get_for_model(self.model)
            messages.add_message(request, messages.ERROR, u"You don't have permissions necessary to edit this page.")
            return HttpResponseRedirect(reverse("admin:%s_%s_changelist" % (ct.app_label, ct.model)))

    def queryset(self, request):
        qs = super(ObjectPermissionMixin, self).queryset(request)
        have_change_perm = [obj.id for obj in qs if self.has_change_permission(request, obj)]
        # Now comes the totally not-hacked-together part
        return qs.filter(id__in = have_change_perm)