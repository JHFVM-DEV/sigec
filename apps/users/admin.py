from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Role

# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'roles', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_staff', 'roles', 'is_doctor', 'is_nurse')
    search_fields = ('email', 'first_name', 'last_name', 'identification_number')
    ordering = ('email', 'identification_number')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles y especialidades', {'fields': ('roles', 'is_doctor', 'is_nurse', 'speciality')}),
        ('Fechas importantes', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'roles', 'is_doctor', 'is_nurse', 'speciality'),
        }),
    )