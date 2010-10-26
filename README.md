Django Per-object Permissions
=============================

Installation
------------

0. perms uses the Django messages framework, so be sure to have Django 1.2 installed.

1. Install the package from Github.

       pip install -e git+git://github.com/ff0000/django-object-permissions.git#egg=perms


2. In your `settings.py` file, add the `AUTHENTICATION_BACKENDS` variable, and set it to

       AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'perms.backends.ObjectPermissionBackend',
       )


3. For each model you want to enforce row-level ACLs, inherit from
   `perms.admin.ObjectPermissionMixin` and add `perms.admin.ObjectPermissionInline`
   as an inline. E.g.

       class MyFlatPageAdmin(ObjectPermissionMixin):
           inlines = [ObjectPermissionInline]

