from django.db import models, connection
from django.utils.text import slugify
from django.db.models import Sum, Count, Avg, F, Case, When, Value, IntegerField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_products_by_category(cls, category_id=None):
        """Get products ordered by price (descending) with optional category filter."""
        query = """
            SELECT p.*, c.name as category_name 
            FROM products_product p
            LEFT JOIN products_category c ON p.category_id = c.id
            {where_clause}
            ORDER BY p.price DESC
        """
        where_clause = "WHERE p.category_id = %s" if category_id else ""
        query = query.format(where_clause=where_clause)
        
        with connection.cursor() as cursor:
            cursor.execute(query, [category_id] if category_id else [])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @classmethod
    def get_product_analytics(cls):
        """
        Get detailed product analytics including:
        - Total value of inventory per category
        - Products below reorder level (stock < 10)
        - Top performing products by stock value
        - Category-wise product count and average price
        """
        # Get inventory summary by category
        inventory_summary = Category.objects.annotate(
            product_count=Count('products'),
            total_stock=Sum('products__stock'),
            total_value=Sum(F('products__stock') * F('products__price')),
            avg_price=Avg('products__price'),
            low_stock_count=Sum(
                Case(
                    When(products__stock__lt=10, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
        ).values(
            'name',
            'product_count',
            'total_stock',
            'total_value',
            'avg_price',
            'low_stock_count'
        )

        # Get top performing products by stock value
        top_products = cls.objects.annotate(
            stock_value=F('stock') * F('price')
        ).select_related('category').order_by('-stock_value')[:5].values(
            'name',
            'category__name',
            'stock',
            'price',
            'stock_value'
        )

        # Get low stock products
        low_stock_products = cls.objects.filter(
            stock__lt=10
        ).select_related('category').order_by('stock').values(
            'name',
            'category__name',
            'stock',
            'price'
        )

        return {
            'inventory_summary': list(inventory_summary),
            'top_products': list(top_products),
            'low_stock_products': list(low_stock_products)
        }

    class Meta:
        ordering = ['-created_at']
