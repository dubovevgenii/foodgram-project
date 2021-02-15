from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Tag, Ingredient, Composition
from .validators import GreaterThanValidator


class CreateRecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all())
    preparing_time = forms.IntegerField(validators=[GreaterThanValidator(0)])

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'preparing_time', 'tags']
        labels = {'title': 'Название рецепта',
                  'image': 'Загрузить фото',
                  'description': 'Описание',
                  'preparing_time': 'Время приготовления',
                  'tags': 'Теги',
                  }
        help_texts = {'title': 'Название рецепта',
                      'image': 'Фото блюда',
                      'description': 'Описание рецепта, порядок приготовления',
                      'preparing_time': 'Время приготовления блюда',
                      }

    def clean(self):
        cleaned_data = super(CreateRecipeForm, self).clean()
        ingredients_list = []
        for param in self.data.keys():
            if 'nameIngredient' in param:
                name, id = param.split('_')
                ingredients_list.append(id)

        if not ingredients_list:
            raise forms.ValidationError('Не выбраны ингредиенты')

        self.cleaned_data['ingredients'] = []
        self.cleaned_data['quantities'] = []

        for id in ingredients_list:
            title = self.data.get(f'nameIngredient_{id}')
            quantity = self.data.get(f'valueIngredient_{id}')

            if int(quantity) <= 0:
                raise forms.ValidationError('Количество не может быть меньше '
                                      'или равно нулю')

            self.cleaned_data['ingredients'].append(title)
            self.cleaned_data['quantities'].append(quantity)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        self.save_m2m()
        ingredients = self.cleaned_data['ingredients']
        quantities = self.cleaned_data['quantities']
        composition_to_del = Composition.objects.filter(recipe_id=instance.id)
        composition_to_del.delete()
        for i in range(0, len(ingredients)):
            ingredient = Ingredient.objects.get(
                title=ingredients[i])
            quantity = quantities[i]
            composition_to_add = Composition(recipe_id=instance.id,
                                             ingredient_id=ingredient.id,
                                             quantity=quantity)
            composition_to_add.save()
        return instance
