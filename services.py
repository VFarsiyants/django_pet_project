import random

from basketapp.models import Basket
from mainapp.models import Product


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.all().filter(is_active=True)

    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]
