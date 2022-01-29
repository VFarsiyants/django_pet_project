from django.test import TestCase

from mainapp.models import ProductCategory, Product


class MainappSmokeTest(TestCase):

    def setUp(self) -> None:
        category = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                category=category,
                name=f'prod#{i}',
                description='desc'
            )

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_categories_urls(self):
        for cat in ProductCategory.objects.all():
            response = self.client.get(f'/products/{cat.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 404)
