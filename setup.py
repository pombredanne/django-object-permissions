from setuptools import setup, find_packages
import sys, os

version = '0.1'

install_requires = ['django>=1.2']

CURRENT_FOLDER = os.path.dirname(__file__)

setup(name='perms',
      version=version,
      description="Gives Django the power of object-level permissions.",
      keywords='django, object permissions',
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      author='Dan Loewenherz',
      author_email='dan.loewenherz+dop@ff0000.com',
      url='http://github.com/ff0000/django-object-permissions',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
)

