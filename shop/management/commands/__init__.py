from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Product, Comment

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for u, p in [('admin', 'S3cr3tAdmin!'), ('alice', 'AlicePass123'),
                     ('bob', 'BobPass456'), ('eve', 'EvilPass789')]:
            if not User.objects.filter(username=u).exists():
                User.objects.create_superuser if u == 'admin' else User.objects.create_user
                (User.objects.create_superuser if u == 'admin' else User.objects.create_user)(
                    username=u, password=p, email=f'{u}@vulnshop.local')
        data = [
            ('Laptop Pro 15', 'High-end laptop with 16GB RAM.', 1299.99, 'Electronics'),
            ('Wireless Mouse', 'Ergonomic 2.4GHz mouse.', 24.50, 'Electronics'),
            ('Coffee Maker', '12-cup programmable coffee maker.', 79.00, 'Home'),
            ('Running Shoes', 'Lightweight shoes for marathon training.', 89.99, 'Sports'),
            ('Desk Lamp', 'LED lamp with USB charging port.', 34.95, 'Home'),
        ]
        for name, desc, price, cat in data:
            prod, _ = Product.objects.get_or_create(
                name=name, defaults={'description': desc, 'price': price, 'category': cat})
            Comment.objects.get_or_create(product=prod, author='alice',
                                          body=f'Great product: {name}!')
        self.stdout.write('Seeded.')