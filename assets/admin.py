from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Asset, Department, MaintenanceLog

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Organization", {"fields": ("department",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Organization", {"fields": ("department",)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Asset)
admin.site.register(Department)
admin.site.register(MaintenanceLog)
