from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe


class CreateRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'preparing_time', 'tags']

        labels = {'name': 'Название рецепта',
                  'image': 'Загрузить фото',
                  'description': 'Описание',
                  'preparing_time': 'Время приготовления',
                  'tags': 'Теги',
                  }
        help_texts = {'name': 'Название рецепта',
                      'image': 'Фото блюда',
                      'description': 'Описание рецепта, порядок приготовления',
                      'preparing_time': 'Время приготовления блюда',
                      }
