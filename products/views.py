from django.shortcuts import render
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, F, Count, Case, When, Value, IntegerField
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class BaseProductQuerySet:
    def get_base_queryset(self):
        return Product.objects.all()

class BaseProductFilter:
    def apply_filters(self, queryset, request):
        search = request.query_params.get('search', None)
        category = request.query_params.get('category', None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListCreateView(generics.ListCreateAPIView, BaseProductQuerySet, BaseProductFilter):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.get_base_queryset()
        return self.apply_filters(queryset, self.request)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductAdvancedSearchView(generics.ListAPIView, BaseProductQuerySet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.get_base_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        stock_status = self.request.query_params.get('stock_status', None)
        if stock_status:
            if stock_status == 'in_stock':
                queryset = queryset.filter(stock__gt=0)
            elif stock_status == 'out_of_stock':
                queryset = queryset.filter(stock=0)
            elif stock_status == 'low_stock':
                threshold = int(self.request.query_params.get('low_stock_threshold', 10))
                queryset = queryset.filter(stock__gt=0, stock__lte=threshold)
        
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        
        # Sorting
        sort_by = self.request.query_params.get('sort_by', None)
        sort_order = self.request.query_params.get('sort_order', 'asc')
        if sort_by:
            if sort_order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 12))
        start = (page - 1) * page_size
        end = start + page_size
        
        # Get counts for statistics
        total_count = queryset.count()
        low_stock_count = queryset.filter(stock__gt=0, stock__lte=10).count()
        out_of_stock_count = queryset.filter(stock=0).count()
        
        # Get paginated results
        paginated_queryset = queryset[start:end]
        serializer = self.get_serializer(paginated_queryset, many=True)
        
        return Response({
            'count': total_count,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'results': serializer.data
        })

class ProductBulkUpdateView(APIView):
    def post(self, request):
        """
        Update stock for multiple products at once.
        Expected format: [{"id": 1, "stock": 10}, {"id": 2, "stock": 20}]
        """
        updates = request.data
        updated_products = []
        
        try:
            for update in updates:
                product = Product.objects.get(id=update['id'])
                product.stock = update['stock']
                product.save()
                updated_products.append(product)
            
            serializer = ProductSerializer(updated_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ProductLowStockView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        threshold = int(self.request.query_params.get('threshold', 10))
        return Product.objects.filter(stock__lt=threshold)

class ProductAnalyticsView(APIView):
    def get(self, request):
        """
        Get comprehensive product analytics including:
        - Inventory value by category
        - Low stock products
        - Top performing products
        """
        try:
            analytics_data = Product.get_product_analytics()
            return Response(analytics_data)
        except Exception as e:
            return Response(
                {'error': f'Error generating analytics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
