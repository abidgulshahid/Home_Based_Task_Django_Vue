<template>
  <div class="dashboard">
    <!-- Header Section -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1>Products</h1>
          <p class="text-subtitle">Manage your product inventory</p>
        </div>
        <div class="header-right">
          <router-link to="/products/create" class="btn-primary">
            <i class="fas fa-plus"></i>
            Add New Product
          </router-link>
        </div>
      </div>
    </div>



    <!-- Filters Section -->
    <div class="filters-section">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search products..."
          @input="debouncedSearch"
        >
      </div>
      <div class="filters-group">
        <div class="filter-item">
          <select v-model="selectedCategory" @change="applyFilters" class="select-input">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="filter-item">
          <select v-model="stockFilter" @change="applyFilters" class="select-input">
            <option value="">All Stock</option>
            <option value="in_stock">In Stock</option>
            <option value="low_stock">Low Stock</option>
            <option value="out_of_stock">Out of Stock</option>
          </select>
        </div>
        <div class="filter-item price-range">
          <input 
            type="number" 
            v-model="minPrice" 
            placeholder="Min Price" 
            @input="debouncedSearch"
            class="number-input"
          >
          <span class="price-separator">-</span>
          <input 
            type="number" 
            v-model="maxPrice" 
            placeholder="Max Price" 
            @input="debouncedSearch"
            class="number-input"
          >
        </div>
        <div class="filter-item">
          <select v-model="sortBy" @change="applyFilters" class="select-input">
            <option value="">Sort By</option>
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="stock">Stock</option>
          </select>
          <select v-model="sortOrder" @change="applyFilters" class="select-input">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>Loading products...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <i class="fas fa-exclamation-circle"></i>
      <p>{{ error }}</p>
    </div>

    <!-- Products Grid -->
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="product-details">
          <div class="product-header">
            <h3>{{ product.name }}</h3>
            <div class="stock-badge" :class="getStockClass(product.stock)">
              {{ product.stock }} in stock
            </div>
          </div>
          <p class="description">{{ product.description }}</p>
          <div class="product-meta">
            <span class="price">${{ formatPrice(product.price) }}</span>
            <span class="category">{{ product.category_name }}</span>
          </div>
          <div class="product-footer">
            <div class="actions">
              <button @click="viewProduct(product)" class="btn-icon" title="View">
                <!-- <i class="fas fa-eye"></i> -->
              </button>
              <button @click="editProduct(product)" class="btn-icon" title="Edit">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="deleteProduct(product.id)" class="btn-icon delete" title="Delete">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button 
        class="btn-page" 
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      <div class="page-numbers">
        <button 
          v-for="page in displayedPages" 
          :key="page"
          class="btn-page"
          :class="{ active: currentPage === page }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
      <button 
        class="btn-page" 
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { debounce } from 'lodash';

export default {
  name: 'ProductList',
  data() {
    return {
      products: [],
      categories: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedCategory: '',
      stockFilter: '',
      minPrice: '',
      maxPrice: '',
      sortBy: '',
      sortOrder: 'asc',
      currentPage: 1,
      itemsPerPage: 12,
      totalProducts: 0,
      lowStockProducts: 0,
      outOfStockProducts: 0
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalProducts / this.itemsPerPage);
    },
    displayedPages() {
      const pages = [];
      const maxPages = 5;
      let start = Math.max(1, this.currentPage - 2);
      let end = Math.min(this.totalPages, start + maxPages - 1);
      
      if (end - start + 1 < maxPages) {
        start = Math.max(1, end - maxPages + 1);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
  },
  created() {
    this.fetchCategories();
    this.fetchProducts();
    this.debouncedSearch = debounce(this.applyFilters, 300);
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('http://localhost:8000/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchProducts() {
      this.loading = true;
      try {
        const params = {
          page: this.currentPage,
          page_size: this.itemsPerPage,
          search: this.searchQuery,
          category: this.selectedCategory,
          stock_status: this.stockFilter,
          min_price: this.minPrice,
          max_price: this.maxPrice,
          sort_by: this.sortBy,
          sort_order: this.sortOrder
        };

        const response = await axios.get('http://localhost:8000/api/products/advanced_search/', { params });
        this.products = response.data.results;
        this.totalProducts = response.data.count;
        this.lowStockProducts = response.data.low_stock_count;
        this.outOfStockProducts = response.data.out_of_stock_count;
      } catch (error) {
        this.error = 'Error loading products';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    applyFilters() {
      this.currentPage = 1;
      this.fetchProducts();
    },
    formatPrice(price) {
      return Number(price).toFixed(2);
    },
    getStockClass(stock) {
      if (stock <= 5) return 'danger';
      if (stock <= 20) return 'warning';
      return 'success';
    },
    editProduct(product) {
      this.$router.push({ name: 'edit-product', params: { id: product.id } });
    },
    viewProduct(product) {
      this.$router.push({ name: 'view-product', params: { id: product.id } });
    },
    async deleteProduct(id) {
      if (confirm('Are you sure you want to delete this product?')) {
        try {
          await axios.delete(`http://localhost:8000/api/products/${id}/`);
          this.fetchProducts();
        } catch (error) {
          console.error(error);
          alert('Error deleting product');
        }
      }
    }
  },
  watch: {
    currentPage() {
      this.fetchProducts();
    }
  }
};
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.text-subtitle {
  color: #718096;
  margin-top: 0.5rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #4f46e5;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #4338ca;
  transform: translateY(-1px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-card.total .stat-icon {
  background-color: #818cf8;
  color: white;
}

.stat-card.low-stock .stat-icon {
  background-color: #fbbf24;
  color: white;
}

.stat-card.out-stock .stat-icon {
  background-color: #ef4444;
  color: white;
}

.stat-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.stat-content p {
  color: #718096;
  margin: 0;
}

.filters-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.search-box {
  position: relative;
  margin-bottom: 1rem;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #718096;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.search-box input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.filters-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-item {
  flex: 1;
  min-width: 200px;
}

.select-input, .number-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  background-color: white;
  transition: all 0.2s;
}

.select-input:focus, .number-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.price-range {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.price-separator {
  color: #718096;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.product-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.product-details {
  padding: 1.5rem;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.product-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  flex: 1;
}

.stock-badge {
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
  white-space: nowrap;
}

.stock-badge.success { background-color: #10b981; }
.stock-badge.warning { background-color: #f59e0b; }
.stock-badge.danger { background-color: #ef4444; }

.description {
  color: #718096;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.875rem;
  line-height: 1.5;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.price {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4f46e5;
}

.category {
  background-color: #f3f4f6;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.product-footer {
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
  margin-top: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 0.375rem;
  color: #718096;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background-color: #f3f4f6;
  color: #1a202c;
}

.btn-icon.delete:hover {
  background-color: #fef2f2;
  color: #ef4444;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.btn-page {
  background: none;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  color: #718096;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-page:hover:not(:disabled) {
  background-color: #f3f4f6;
  color: #1a202c;
}

.btn-page.active {
  background-color: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #718096;
}

.loader {
  border: 3px solid #f3f4f6;
  border-radius: 50%;
  border-top: 3px solid #4f46e5;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #ef4444;
}

.error-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}
</style> 