from django.db import models

class Category(models.Model):
    name =  models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']



class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(blank=True, null=True, upload_to='static/images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена покупки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']




