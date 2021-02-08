from rest_framework import serializers
from recipes.models import Favorite, Subscribe, Purchase


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model"""
    id = serializers.IntegerField(source='recipe_id')
    user = serializers.IntegerField(source='user_id', required=False)

    class Meta:
        fields = ['id', 'user']
        model = Favorite


class SubscribeSerializer(serializers.ModelSerializer):
    """Serializer for Subscribe model"""
    id = serializers.IntegerField(source='author_id')
    user = serializers.IntegerField(source='user_id', required=False)

    class Meta:
        fields = ['id', 'user']
        model = Subscribe


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase model"""
    id = serializers.IntegerField(source='recipe_id')
    user = serializers.IntegerField(source='user_id', required=False)

    class Meta:
        fields = ['id', 'user']
        model = Purchase
