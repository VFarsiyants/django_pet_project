import random
from django.urls import reverse
from django.conf import settings
from mainapp.models import Product
from django.core.mail import send_mail


def get_hot_product():
    product_list = Product.objects.all().filter(is_active=True)

    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'{settings.BASE_URL}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
