from django.shortcuts import render
from django.conf import settings
import json

from mainapp.models import Product, ProductCategory


def index(request):

    products_list = Product.objects.all()[:3]
    print(products_list.query)

    context = {
        'title': 'Мой магазин',
        'products': products_list
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    links_products_menu = ProductCategory.objects.all()
    context = {
        'links_products_menu': links_products_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json') as contacts_file:
        context = {
            'contacts': json.load(contacts_file)
        }
    return render(request, 'mainapp/contact.html', context)
