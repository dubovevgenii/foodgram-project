from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Favorite, Subscribe, Purchase, Ingredient
from .serializers import (FavoriteSerializer, SubscribeSerializer,
                          PurchaseSerializer)


class CustomAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    TRUE_RESPONSE = {'success': True}
    FALSE_RESPONSE = {'success': False}


class FavoriteDetail(CustomAPIView):
    """View for favorite model API."""
    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(self.TRUE_RESPONSE)
        return JsonResponse(self.FALSE_RESPONSE)

    def delete(self, request, pk):
        favorite = get_object_or_404(Favorite, recipe_id=pk,
                                     user=request.user)
        favorite.delete()
        return JsonResponse(self.TRUE_RESPONSE)


class SubscribeDetail(CustomAPIView):
    """View for subscribe model API."""
    def post(self, request):
        serializer = SubscribeSerializer(data=request.data,
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(self.TRUE_RESPONSE)
        return JsonResponse(self.FALSE_RESPONSE)

    def delete(self, request, pk):
        subscribe = get_object_or_404(Subscribe, author_id=pk,
                                      user=request.user)
        subscribe.delete()
        return JsonResponse(self.TRUE_RESPONSE)


class PurchaseDetail(CustomAPIView):
    """View for subscribe model API."""
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.is_authenticated:
                cart = request.session['cart']
                cart.append(request.data['id'])
                request.session['cart'] = cart
                return JsonResponse(self.TRUE_RESPONSE)
            else:
                serializer.save(user=request.user)
                return JsonResponse(self.TRUE_RESPONSE)
        return JsonResponse(self.FALSE_RESPONSE)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            cart = request.session['cart']
            cart.remove(str(pk))
            request.session['cart'] = cart
            return JsonResponse(self.TRUE_RESPONSE)
        else:
            purchase = get_object_or_404(Purchase, recipe_id=pk,
                                         user=request.user)
            purchase.delete()
            return JsonResponse(self.TRUE_RESPONSE)


@api_view(['GET'])
@csrf_protect
def ingredients(request):
    """View for ingredient autocomplete in new/edit recipe page."""
    ingredient_part = request.GET.get('query')
    suggestion = (
        Ingredient.objects.annotate(dimension=F('unit'))
        .filter(title__istartswith=ingredient_part)
        .values('title', 'dimension')
    )
    return Response(suggestion)
