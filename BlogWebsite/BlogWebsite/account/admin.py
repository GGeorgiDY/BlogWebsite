from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


@admin.register(AppUser)
class AccountAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('pk', 'email', 'username',)
    # fields that will be read only and should never be changed
    readonly_fields = ('pk', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# admin.site.register(AppUser, AccountAdmin)
