from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'
    ordering = '-is_active'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:users')


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:users')


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'
    ordering = '-is_active'


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount/100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products_list.html'

    def _getcategory(self):
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(ProductCategory, pk=category_id)
        return category

    def get_queryset(self):
        return Product.objects.all().filter(category__pk=self._getcategory().pk).order_by('-is_active')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/product_form.html'
    success_url = reverse_lazy('adminapp:categories')

    def _getcategory(self):
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(ProductCategory, pk=category_id)
        return category

    def get_success_url(self):
        return reverse('adminapp:products', args=[self._getcategory().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._getcategory()
        return context_data


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/product_form.html'
    success_url = reverse_lazy('adminapp:categories')

    def _getcategory(self):
        category_id = self.kwargs.get('category_pk')
        category = get_object_or_404(ProductCategory, pk=category_id)
        return category

    def get_success_url(self):
        return reverse('adminapp:products', args=[self._getcategory().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._getcategory()
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('adminapp:products')

    def _getcategory(self):
        category_id = self.kwargs.get('category_pk')
        category = get_object_or_404(ProductCategory, pk=category_id)
        return category

    def get_success_url(self):
        return reverse('adminapp:products', args=[self._getcategory().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._getcategory()
        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'
