from django.contrib import admin

from recipes.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email')
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
