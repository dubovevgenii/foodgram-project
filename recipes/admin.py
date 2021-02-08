from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import Ingredient, Recipe, Favorite


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit')
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    def favorites__count(obj):
        return Favorite.objects.filter(recipe=obj).count()

    list_display = ('pk', 'title', 'author', 'favorites__count')
    list_filter = ('title', 'author', 'tags')
    empty_value_display = '-пусто-'
    readonly_fields = ('favorites__count',)
    fieldsets = (
        (None, {
            'fields':
                ('author', 'title', 'image', 'description', 'tags',
                 'favorites__count')
        }),
    )


models_dict = apps.all_models['recipes']
for model in models_dict.values():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
