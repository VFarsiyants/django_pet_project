from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_quantity

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()

        super(Basket, self).delete()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
