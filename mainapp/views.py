from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from services import get_basket, get_hot_product, get_same_products


def index(request):
    products_list = Product.objects.all().filter(is_active=True)[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    links_products_menu = ProductCategory.objects.all().filter(is_active=True)
    hot_product = get_hot_product()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().filter(is_active=True)
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).filter(is_active=True)
        context = {
            'links_products_menu': links_products_menu,
            'products': products_list,
            'category': category_item,
            'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', context)
    context = {
        'links_products_menu': links_products_menu,
        'title': 'Товары',
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'basket': get_basket(request.user)
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_products_menu = ProductCategory.objects.all().filter(is_active=True)
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_products_menu': links_products_menu,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)
