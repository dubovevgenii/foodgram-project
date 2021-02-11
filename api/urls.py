from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.FavoriteDetail.as_view(), name='api_favorites'),
    path('favorites/<int:pk>/', views.FavoriteDetail.as_view(),
         name='api_favorites_del'),
    path('subscribes/', views.SubscribeDetail.as_view(),
         name='api_subscribes'),
    path('subscribes/<int:pk>/', views.SubscribeDetail.as_view(),
         name='api_subscribes_del'),
    path('purchases/', views.PurchaseDetail.as_view(), name='api_purchases'),
    path('purchases/<int:pk>/', views.PurchaseDetail.as_view(),
         name='api_purchases_del'),
    path('ingredients/', views.ingredients, name='api_ingredients'),
]
