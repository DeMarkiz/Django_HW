from django.core.management.base import BaseCommand
from catalog.models import Category, Product



class Command(BaseCommand):
    help = 'Add product to database'
    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(name='мясо', description='мясо')



        product = [
            {'name': 'Курица', 'purchase_price': '199', 'category':category},
            {'name': 'говядина', 'purchase_price': '399', 'category':category},


        ]

        for product_data in product:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'ready: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'not ready: {product.name}'))
