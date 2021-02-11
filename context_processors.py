from recipes.models import Purchase, Tag, Recipe


def counter(request):
    """Function returning items count in cart."""
    if request.user.is_authenticated:
        in_purchases = Purchase.objects.filter(user=request.user)
    else:
        if request.session.get('cart', []):
            cart = request.session['cart']
            in_purchases = Recipe.objects.filter(pk__in=cart)
        else:
            in_purchases = []

    if in_purchases:
        return {'counter': len(in_purchases)}
    else:
        return {'counter': ''}


def get_tags(request):
    """Function enabling tags context on any page."""
    return {'tags': Tag.objects.all()}





# def url_filters(request):
#     filters = request.GET.getlist('filters')
#     filters.insert(0, '')
#     filters = '&filters='.join(filters)
#     return {'filters': filters}
