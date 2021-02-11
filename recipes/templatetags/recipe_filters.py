from django import template

from recipes.models import Purchase, Favorite

register = template.Library()


@register.filter
def in_purchases_auth(recipe, user):
    exam = Purchase.objects.filter(user=user, recipe=recipe).exists()
    return exam


@register.filter
def in_purchases_not_auth(recipe, request):
    if request.session.get('cart', []):
        cart = request.session['cart']
        exam = str(recipe.id) in cart
    else:
        request.session['cart'] = []
        exam = False
    return exam


@register.filter
def in_favorites(recipe, user):
    exam = Favorite.objects.filter(user=user, recipe=recipe).exists()
    return exam


@register.filter
def recipe_cases(number):
    text_forms = ['рецепт', 'рецепта', 'рецептов']
    number = number - 3
    n_10 = number % 100
    n_1 = n_10 % 10
    if 10 < n_10 < 20:
        case = text_forms[2]
    elif 1 < n_1 < 5:
        case = text_forms[1]
    elif n_1 == 1:
        case = text_forms[0]
    else:
        case = text_forms[2]
    return f'Еще {number} {case}...'
