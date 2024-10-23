from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from myapp.models import *
from django.contrib.auth.models import AbstractUser

admin.site.register(Ward)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(History)
admin.site.register(Service)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'name', 'adhar_no', 'ward_no', 'house_no', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'name', 'adhar_no', 'ward_no', 'house_no', 'role')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'is_active', 'is_approved', 'role', 'date_joined')
    search_fields = ('email', 'username')

    # Define the fieldsets for the user detail view (when editing an existing user)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('name', 'email', 'adhar_no', 'ward_no', 'house_no', 'dob', 'profile_pic', 'cover_pic','service')}),
        ('Permissions', {'fields': ('is_active', 'is_approved', 'role', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields for adding a new user (include the custom fields here)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'password1', 'password2', 'name', 'adhar_no', 'ward_no', 'house_no', 'dob', 'role',
            'is_active', 'is_approved','service')}
         ),
    )


# Register the CustomUser model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
