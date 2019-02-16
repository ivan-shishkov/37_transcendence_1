from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

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


class FriendsCountListFilter(admin.SimpleListFilter):
    title = 'friends count'
    parameter_name = 'friends_count'

    def lookups(self, request, model_admin):
        return (
            ('0', 'no friends'),
            ('1-9', 'from 1 to 9'),
            ('10-19', 'from 10 to 19'),
            ('20-49', 'from 20 to 49'),
            ('50-99', 'from 50 to 99'),
            ('100_and_more', 'from 100 and more'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(Count('friends'))

        query_parameter = self.value()

        if query_parameter == '0':
            return queryset.filter(friends__count=0)

        if query_parameter == '100_and_more':
            return queryset.filter(friends__count__gte=100)

        if query_parameter and '-' in query_parameter:
            min_value, max_value = query_parameter.split('-')

            return queryset.filter(
                friends__count__gte=int(min_value),
                friends__count__lte=int(max_value),
            )


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_filter = (HavingAvatarListFilter, FriendsCountListFilter)


admin.site.register(CustomUser, CustomUserAdmin)
