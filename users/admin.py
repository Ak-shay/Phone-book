from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'email', 'phone', 'age')}), #fields while creating user from admin
    )
    list_display = ['username', 'age' , 'phone', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'phone')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'age')}), #added custom fields to display
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )

admin.site.register(CustomUser, CustomUserAdmin)
