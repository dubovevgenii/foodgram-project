import io
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (ListView, DetailView, CreateView,
                                  DeleteView, UpdateView)
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from foodgram.settings import ELEMENTS_PER_PAGE
from users.models import User
from .forms import CreateRecipeForm
from .models import Recipe, Composition, Purchase


class RecipeListView(ListView):
    """View-function for index page (url "")."""
    paginate_by = ELEMENTS_PER_PAGE
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        self.tags = self.request.GET.get('filter')
        if self.tags and sorted(self.tags) == ['b', 'd', 'l']:
            return redirect('index')
        return super(RecipeListView, self).get(*args, **kwargs)

    def get_queryset(self):
        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            return Recipe.objects.all()
        else:
            tags_to_filter = []
            if 'b' in self.tags:
                tags_to_filter.append('breakfast')
            if 'l' in self.tags:
                tags_to_filter.append('lunch')
            if 'd' in self.tags:
                tags_to_filter.append('dinner')
            return Recipe.objects.filter(
                tags__title__in=tags_to_filter).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            context['filter'] = 'bdl'
        else:
            context['filter'] = self.tags
        return context


class RecipeDetailView(DetailView):
    """View-function for recipe page (url "recipe/slug/edit")."""
    model = Recipe
    template_name = 'recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_list'] = Composition.objects.filter(
            recipe_id__slug=self.kwargs['slug'])
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """View-function for recipe page creation (url "new")."""
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'recipe_form.html'

    def get_success_url(self):
        return reverse('recipe', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super(RecipeCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compositions'] = Composition.objects.filter()
        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """View-function for recipe updating (url "recipe/<slug:slug>/edit")."""
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'recipe_form.html'

    def get_success_url(self):
        return reverse('recipe', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compositions'] = Composition.objects.filter(
            recipe=self.object)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super(RecipeUpdateView, self).form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    """View-function for recipe deleting (url "recipe/<slug:slug>/delete")."""
    model = Recipe
    template_name = 'misc/delete_account.html'
    success_url = reverse_lazy('index')


class ProfileListView(ListView):
    """View-function for profile page (url "username")."""
    paginate_by = ELEMENTS_PER_PAGE
    template_name = 'profile.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        self.tags = self.request.GET.get('filter')

        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            return Recipe.objects.filter(author=self.user)
        else:
            tags_to_filter = []
            if 'b' in self.tags:
                tags_to_filter.append('breakfast')
            if 'l' in self.tags:
                tags_to_filter.append('lunch')
            if 'd' in self.tags:
                tags_to_filter.append('dinner')
            return Recipe.objects.filter(
                author=self.user, tags__title__in=tags_to_filter).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user

        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            context['filter'] = 'bdl'
        else:
            context['filter'] = self.tags
        return context


class SubscribeListView(LoginRequiredMixin, ListView):
    """View-function for subscriptions (url "subscribes")."""
    paginate_by = ELEMENTS_PER_PAGE
    template_name = 'follow.html'

    def get_queryset(self):
        return User.objects.filter(
            subscribing__user=self.request.user).order_by('username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FavoriteListView(LoginRequiredMixin, ListView):
    """View-function for favorites (url "favorites")."""
    paginate_by = ELEMENTS_PER_PAGE
    template_name = 'favorite.html'

    def get_queryset(self):
        self.tags = self.request.GET.get('filter')
        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user)
        else:
            tags_to_filter = []
            if 'b' in self.tags:
                tags_to_filter.append('breakfast')
            if 'l' in self.tags:
                tags_to_filter.append('lunch')
            if 'd' in self.tags:
                tags_to_filter.append('dinner')
        return Recipe.objects.filter(favorite_recipe__user=self.request.user,
                                     tags__title__in=tags_to_filter).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.tags or sorted(self.tags) == ['b', 'd', 'l']:
            context['filter'] = 'bdl'
        else:
            context['filter'] = self.tags
        return context


class PurchaseListView(ListView):
    """View-function for shopping list (url "purchases")."""
    template_name = 'shopList.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(
                purchase_recipe__user=self.request.user)
        else:
            cart = self.request.session['cart']
            return Recipe.objects.filter(pk__in=cart)


class PurchaseDeleteView(DeleteView):
    """
    View-function for deleting purchases from shopping list
    (url "purchases/<int:pk>/").
    """
    model = Purchase
    success_url = reverse_lazy("shopping_index")


@csrf_protect
def purchases(request):
    if request.user.is_authenticated:
        user_cart = Purchase.objects.filter(user=request.user)\
            .values_list('recipe_id', flat=True)
        purchases = Composition.objects.filter(recipe__in=user_cart)\
            .values('ingredient__title', 'ingredient__unit')\
            .annotate(total=Sum('quantity'))
    else:
        cart = request.session['cart']
        purchases = Composition.objects.filter(recipe_id__in=cart)\
            .values('ingredient__title', 'ingredient__unit')\
            .annotate(total=Sum('quantity'))
    today = date.today()
    filename = str(request.user.username) + today.strftime('%Y-%m-%d')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    font_object = ttfonts.TTFont('Arial', './static/fonts/arial_cyr.ttf')
    pdfmetrics.registerFont(font_object)
    p.setFont("Arial", 9)
    p.drawString(20, 800, 'Список покупок')

    number = 0
    x = 740
    for i in purchases:
        number += 1
        number_par = str(number)
        ingredient_par = str(i['ingredient__title'])
        quantity_par = str(i['total'])
        unit_par = str(i['ingredient__unit'])
        x -= 20
        p.drawString(20, x, f'{number_par}. {ingredient_par} '
                            f'({unit_par}) - {quantity_par}')

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)


def page_not_found(request, exception):
    """View-function for page not found exception (404)."""
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    """View-function for server error page exception (500)."""
    return render(request, 'misc/500.html', status=500)
