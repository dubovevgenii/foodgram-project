from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import GreaterThanValidator
from users.models import User


class Ingredient(models.Model):
    """Ingredient model."""

    title = models.CharField(verbose_name='название ингредиента',
                             max_length=200, db_index=True)
    unit = models.CharField(max_length=15, verbose_name='единица')

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'игредиенты'
        ordering = ['title']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag model (necessary for multiselection possibility)."""
    title = models.CharField(max_length=20, verbose_name='название тега')
    display_name = models.CharField(max_length=20,
                                    verbose_name='имя тега для отображения')
    color = models.CharField(max_length=20,
                             verbose_name='цвет для отображения')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Recipe model."""

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe_user',
                               verbose_name='автор публикации')
    title = models.CharField(verbose_name='название рецепта', max_length=200)
    image = models.ImageField(verbose_name='картинка', upload_to='images/')
    description = models.TextField(verbose_name='описание')
    ingredient = models.ManyToManyField(Ingredient, through='Composition',
                                        related_name='recipe_ingredient',
                                        verbose_name='ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipe_tag',
                                  verbose_name='теги')
    preparing_time = models.PositiveSmallIntegerField(
        validators=[GreaterThanValidator(0)],
        verbose_name='время приготовления в минутах')
    slug = AutoSlugField(populate_from='title', allow_unicode=True,
                         unique=True)
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Composition(models.Model):
    """Composition of dish with quantity of every ingredient."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='compos_recipe',
                               verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='compos_ingredient',
                                   verbose_name='ингредиент')
    quantity = models.DecimalField(max_digits=6, decimal_places=2,
                                   verbose_name='количество',
                                   validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ['recipe', 'ingredient']
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецепта'


class Subscribe(models.Model):
    """Subscribing for authors model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscriber')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='subscribing')

    class Meta:
        unique_together = ['user', 'author']
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Favorite(models.Model):
    """Favorite recipes model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipe')

    class Meta:
        unique_together = ['user', 'recipe']
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'


class Purchase(models.Model):
    """Shopping list model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchase_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchase_recipe')

    class Meta:
        unique_together = ['user', 'recipe']
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
