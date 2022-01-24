from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json
from django.views.generic import ListView

from mainapp.models import Product, ProductCategory
from services import get_hot_product, get_same_products


class IndexView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        return super(IndexView, self).get_queryset().filter(is_active=True).select_related()[:4]

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(IndexView, self).get_context_data()
        context_data['title'] = 'Мой магазин'
        return context_data


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
            'product': get_object_or_404(Product, pk=self.kwargs.get('pk')),
            'links_products_menu': ProductCategory.objects.all().filter(is_active=True)
        }
        return context_data
