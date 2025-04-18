from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductAdvancedSearchView,
    ProductBulkUpdateView,
    ProductLowStockView,
    ProductAnalyticsView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView
)

urlpatterns = [
    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('products/advanced_search/', ProductAdvancedSearchView.as_view(), name='product-advanced-search'),
    path('products/bulk-update/', ProductBulkUpdateView.as_view(), name='product-bulk-update'),
    path('products/low-stock/', ProductLowStockView.as_view(), name='product-low-stock'),
    path('products/analytics/', ProductAnalyticsView.as_view(), name='product-analytics'),
    
    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
] 