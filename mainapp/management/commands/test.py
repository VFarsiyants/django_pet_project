from django.core.management import BaseCommand

from authapp.models import ShopUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            print(user.email)

