from django.test import TestCase

from authapp.models import ShopUser


class UserAuthTestCase(TestCase):
    username = 'django'
    password = 'geekbrains'
    email = 'django@gb.local'

    def setUp(self) -> None:
        self.user = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')

        self.assertFalse(response.context['user'].is_anonymous)

        self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_basket_auth_redirect(self):
        self.client.get('/auth/logout/')
        response = self.client.get('/basket/')
        self.assertTrue(response.status_code, 302)
