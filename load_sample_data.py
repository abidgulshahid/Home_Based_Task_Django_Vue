import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product

def create_sample_data():
    # Create categories
    categories = [
        Category.objects.create(name='Electronics', description='Electronic devices and accessories'),
        Category.objects.create(name='Clothing', description='Fashion and apparel'),
        Category.objects.create(name='Books', description='Books and literature'),
    ]

    # Create products
    products_data = [
        {'name': 'Smartphone', 'price': 999.99, 'stock': 50},
        {'name': 'Laptop', 'price': 1299.99, 'stock': 30},
        {'name': 'T-shirt', 'price': 19.99, 'stock': 100},
        {'name': 'Jeans', 'price': 49.99, 'stock': 75},
        {'name': 'Python Programming', 'price': 39.99, 'stock': 20},
        {'name': 'Django for Beginners', 'price': 29.99, 'stock': 15},
    ]

    for product_data in products_data:
        Product.objects.create(
            **product_data,
            category=random.choice(categories),
            description=f"Sample description for {product_data['name']}"
        )

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data() 