from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class HavingAvatarListFilter(admin.SimpleListFilter):
    title = 'having avatar'
    parameter_name = 'having_avatar'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'have avatar'),
            ('no', 'no avatar'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(avatar='')

        if self.value() == 'no':
            return queryset.filter(avatar='')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_filter = (HavingAvatarListFilter,)


admin.site.register(CustomUser, CustomUserAdmin)
