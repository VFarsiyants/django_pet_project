from django.contrib import admin

from basketapp.models import Basket
from .models import ProductCategory, Product


admin.site.register(Basket)
admin.site.register(ProductCategory)
admin.site.register(Product)
