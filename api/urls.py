from django.urls import path

from . import views

urlpatterns = [
    path('favorites/', views.favorite_post),
    path('favorites/<int:pk>/', views.favorite_delete),
    path('subscribes/', views.subscribe_post),
    path('subscribes/<int:pk>/', views.subscribe_delete),
    path('purchases/', views.purchase_post),
    path('purchases/<int:pk>/', views.purchase_delete),
    path('ingredients/', views.ingredients),
]