from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json

from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from mainapp.models import Product, ProductCategory
from services import get_hot_product, get_same_products
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products in category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
                order_by('price')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


class IndexView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        # return super(IndexView, self).get_queryset().filter(is_active=True).select_related()[:4]
        return get_products().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(IndexView, self).get_context_data()
        context_data['title'] = 'Мой магазин'
        return context_data


@cache_page(3600)
def products(request, pk=None, page=1):
    links_products_menu = get_links_menu()
    hot_product = get_hot_product()

    if pk is not None:
        if pk == 0:
            products_list = get_products()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_category(pk=pk)
            products_list = Product.objects.filter(category__pk=pk).filter(is_active=True)

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_products_menu': links_products_menu,
            'products': products_paginator,
            'category': category_item
        }
        return render(request, 'mainapp/products_list.html', context)
    context = {
        'links_products_menu': links_products_menu,
        'title': 'Товары',
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product)
    }
    return render(request, 'mainapp/products.html', context)


class ContactsView(ListView):
    template_name = 'mainapp/contact.html'

    def get_queryset(self):
        return

    def get_context_data(self, *, object_list=None, **kwargs):
        with open(f'{settings.BASE_DIR}/contacts.json') as contacts_file:
            context_data = {
                'contacts': json.load(contacts_file)
            }
        return context_data


class ProductView(ListView):
    template_name = 'mainapp/product.html'

    def get_queryset(self):
        return

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = {
            'product': get_product(pk=self.kwargs.get('pk')),
            'links_products_menu': get_links_menu()
        }
        return context_data
