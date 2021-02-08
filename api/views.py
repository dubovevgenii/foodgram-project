from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from recipes.models import Favorite, Subscribe, Purchase, Ingredient
from .serializers import FavoriteSerializer, SubscribeSerializer, \
    PurchaseSerializer


@api_view(['POST'])
@csrf_protect
def favorite_post(request):
    """View for including recipe in favorites."""
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)
    return Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@csrf_protect
def favorite_delete(request, pk):
    """View for removing recipe from favorites."""
    favorite = get_object_or_404(Favorite, recipe_id=pk, user=request.user)
    favorite.delete()
    return Response({'success': 'true'})


@api_view(['POST'])
@csrf_protect
def subscribe_post(request):
    """View for including author in subscribing."""
    serializer = SubscribeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)
    return Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@csrf_protect
def subscribe_delete(request, pk):
    """View for removing author from subscribing."""
    follow = get_object_or_404(Subscribe, author_id=pk, user=request.user)
    follow.delete()
    return Response({'success': 'true'})


@api_view(['POST'])
@csrf_protect
def purchase_post(request):
    """View for including recipe in shopping cart."""
    if not request.user.is_authenticated:
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            cart = request.session['cart']
            cart.append(request.data['id'])
            request.session['cart'] = cart
            return Response({'success': 'true'},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'false'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success': 'true'},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'false'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@csrf_protect
def purchase_delete(request, pk):
    """View for removing recipe from shopping cart."""
    if not request.user.is_authenticated:
        cart = request.session['cart']
        cart.remove(str(pk))
        request.session['cart'] = cart
        return Response({'success': 'true'})
    else:
        follow = get_object_or_404(Purchase, recipe_id=pk, user=request.user)
        follow.delete()
        return Response({'success': 'true'})


@api_view(['GET'])
@csrf_protect
def ingredients(request):
    """View for ingredient autocomplete in new/edit recipe page."""
    ingredient_part = request.GET.get('query')
    suggestion = Ingredient.objects\
        .extra(select={'dimension': 'unit'})\
        .filter(title__startswith=ingredient_part)\
        .values('title', 'dimension')
    return Response(suggestion)
