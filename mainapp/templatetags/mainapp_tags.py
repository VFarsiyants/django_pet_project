from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='product_image')
def product_image(image):
    if not image:
        image = 'products_images/default_product.png'
    return f'{settings.MEDIA_URL}{image}'
