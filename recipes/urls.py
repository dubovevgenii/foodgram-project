from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('subscribes/', views.SubscribeListView.as_view(),
         name='subscribes_index'),
    path('favorites/', views.FavoriteListView.as_view(),
         name='favorites_index'),
    path('purchases/', views.PurchaseListView.as_view(),
         name='purchases_index'),
    path('purchases-pdf/', views.purchases, name='return_pdf'),
    path('purchases/<int:pk>/', views.PurchaseDeleteView.as_view(),
         name='shopping_delete'),
    path('<str:username>/', views.ProfileListView.as_view(), name='profile'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(),
         name='recipe'),
    path('recipe/<slug:slug>/edit/', views.RecipeUpdateView.as_view(),
         name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', views.RecipeDeleteView.as_view(),
         name='recipe_delete'),
    path('', views.RecipeListView.as_view(), name='index'),
]
