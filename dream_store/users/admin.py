from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, UserProfile


class UserAdmin(BaseUserAdmin):
    """
    Переопределенное представление страницы пользователей для admin панели.
    """

    list_display = ('id', 'email',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1',
                       'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Админа для профилей пользователей.
    """

    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'about',)
    search_fields = ('email',)
    ordering = ('-id',)
