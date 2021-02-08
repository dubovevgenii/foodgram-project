# Generated by Django 3.0.8 on 2021-02-05 20:07

import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='количество')),
            ],
            options={
                'verbose_name': 'ингредиент рецепта',
                'verbose_name_plural': 'ингредиенты рецепта',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='название ингредиента')),
                ('unit', models.CharField(max_length=15, verbose_name='единица')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'игредиенты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='название тега')),
                ('display_name', models.CharField(max_length=20, verbose_name='имя тега для отображения')),
                ('color', models.CharField(max_length=20, verbose_name='цвет для отображения')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название рецепта')),
                ('image', models.ImageField(upload_to='images/', verbose_name='картинка')),
                ('description', models.TextField(verbose_name='описание')),
                ('preparing_time', models.PositiveSmallIntegerField(verbose_name='время приготовления в минутах')),
                ('slug', autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from='title', unique=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_user', to=settings.AUTH_USER_MODEL, verbose_name='автор публикации')),
                ('ingredient', models.ManyToManyField(related_name='recipe_ingredient', through='recipes.Composition', to='recipes.Ingredient', verbose_name='ингредиенты')),
                ('tags', models.ManyToManyField(related_name='recipes_tag', to='recipes.Tag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddField(
            model_name='composition',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compos_ingredient', to='recipes.Ingredient', verbose_name='ингредиент'),
        ),
        migrations.AddField(
            model_name='composition',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compos_recipe', to='recipes.Recipe', verbose_name='рецепт'),
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
                'unique_together': {('user', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_recipe', to='recipes.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'покупка',
                'verbose_name_plural': 'покупки',
                'unique_together': {('user', 'recipe')},
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipe', to='recipes.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранные',
                'unique_together': {('user', 'recipe')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='composition',
            unique_together={('recipe', 'ingredient')},
        ),
    ]