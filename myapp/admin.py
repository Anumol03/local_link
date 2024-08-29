from django.contrib import admin
from myapp.models import *
from django.contrib.auth.models import AbstractUser

admin.site.register(Ward)
admin.site.register(CustomUser)


