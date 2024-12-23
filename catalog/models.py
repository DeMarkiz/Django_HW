from django.db import models
from users.models import CustomUser


class Category(models.Model):
    """Модель для описания категорий"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    """Модель для описания продуктов"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.CharField(max_length=200, verbose_name='Описание')
    image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    price = models.IntegerField(verbose_name='Цена')
    is_published = models.BooleanField(default=False, verbose_name="Статус публикации")
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_products", verbose_name="Владелец")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        permissions = [("can_unpublish_product", "Can unpublish product"),]
