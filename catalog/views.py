from django.http import HttpResponse, HttpResponseForbidden
from unicodedata import category

from .models import Product, Category
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView, View
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_products_by_category
from django.core.cache import cache

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        product = super().get_object()
        if product.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не можете изменять этот продукт")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        product = super().get_object()
        if product.owner == self.request.user or request.user.has_perm("catalog.delete_product"):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не можете удалить этот продукт")


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Ключ для кеша
        cache_key = 'product_list'

        # Попытка получить список продуктов из кэша
        cached_products = cache.get(cache_key)

        if not cached_products:
            # Если продуктов в кеше нет, получаем их из базы данных
            cached_products = Product.objects.all()
            # Сохраняем список продуктов в кэш на 15 минут
            cache.set(cache_key, cached_products, timeout=60 * 15)

        return cached_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_moderator = self.request.user.groups.filter(name="Модератор продуктов").exists()
        context["is_moderator"] = is_moderator
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет прав для снятия продукта с публикации")
        product.is_published = False
        product.save()
        return redirect("catalog:product_list")


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"

    @staticmethod
    def post(request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"{name}, указанные Вами телефон и сообщение получены<br>Телефон: {phone}<br>Сообщение: {message}"
        )

class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)
