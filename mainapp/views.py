from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json

from mainapp.models import Product, ProductCategory
from services import get_hot_product, get_same_products


def index(request):
    products_list = Product.objects.all().filter(is_active=True)[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None, page=1):
    links_products_menu = ProductCategory.objects.all().filter(is_active=True)
    hot_product = get_hot_product()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().filter(is_active=True)
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
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


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json') as contacts_file:
        context = {
            'contacts': json.load(contacts_file)
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_products_menu = ProductCategory.objects.all().filter(is_active=True)
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_products_menu': links_products_menu
    }
    return render(request, 'mainapp/product.html', context)
