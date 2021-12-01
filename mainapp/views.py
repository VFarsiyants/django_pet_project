from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def index(request):
    # duplicated code
    items_qty = None
    total = None
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        if basket:
            items_qty = sum(basket.values_list('quantity', flat=True))
            total = sum([item.product.price * item.quantity for item in basket])
    # duplicated code
    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list,
        'item_qty': items_qty,
        'total': total
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    links_products_menu = ProductCategory.objects.all()
    items_qty = None
    total = None
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        if basket:
            items_qty = sum(basket.values_list('quantity', flat=True))
            total = sum([item.product.price * item.quantity for item in basket])
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)
        context = {
            'links_products_menu': links_products_menu,
            'products': products_list,
            'category': category_item,
            'item_qty': items_qty,
            'total': total
        }
        return render(request, 'mainapp/products_list.html', context)
    context = {
        'links_products_menu': links_products_menu,
        'title': 'Товары',
        'hot_product': Product.objects.all().first(),
        'same_products': Product.objects.all()[1:4],
        'item_qty': items_qty,
        'total': total
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json') as contacts_file:
        context = {
            'contacts': json.load(contacts_file)
        }
    return render(request, 'mainapp/contact.html', context)
