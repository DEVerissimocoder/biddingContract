from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Unregister o User padrão do Django
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active']
    actions = ['add_permission']

    def add_permission(self, request, queryset):
        for user in queryset:
            user.is_active = True
            user.save()

# Registrar o User com o CustomUserAdmin
admin.site.register(User, CustomUserAdmin)