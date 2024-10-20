from django.contrib import admin
from myapp.models import *
from django.contrib.auth.models import AbstractUser

admin.site.register(Ward)
admin.site.register(CustomUser)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(History)
admin.site.register(Service)


