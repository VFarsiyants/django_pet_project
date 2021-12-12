from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='имя продукта')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='изображение')
    short_desc = models.CharField(max_length=60, blank=True, verbose_name='краткое описание продукта')
    description = models.TextField(blank=True, verbose_name='описание продукта')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='цена продукта')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество на складе')
    is_active = models.BooleanField(default=True, verbose_name='активен')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

