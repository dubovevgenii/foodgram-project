from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import Ingredient, Recipe, Favorite


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Setting up ingredient model for admin site."""
    list_display = ('pk', 'title', 'unit')
    list_filter = ('title',)
    empty_value_display = '-пусто-'
    search_fields = ['title']


class IngredientInline(admin.TabularInline):
    """Setting up intermediate ingredient class for recipe inline."""
    model = Recipe.ingredient.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Setting up recipe model for admin site."""

    def favorites__count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorites__count.short_description = 'число добавлений в избранное'
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
    inlines = [IngredientInline]
    autocomplete_fields = ['ingredient']


models_dict = apps.all_models['recipes']
for model in models_dict.values():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
