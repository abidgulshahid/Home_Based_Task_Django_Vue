<template>
  <div class="dashboard">
    <!-- Navigation Breadcrumb -->
    <div class="breadcrumb">
      <h1>E-commerce Dashboard</h1>
      <div class="nav-links">
        <router-link to="/" class="nav-link active">Products</router-link>
        <span class="separator">+</span>
        <span class="current">{{ isEdit ? 'Edit Product' : 'Create Product' }}</span>
      </div>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h2>{{ isEdit ? 'Edit Product' : 'Create Product' }}</h2>
          <p class="subtitle">{{ isEdit ? 'Update product information' : 'Add a new product to your inventory' }}</p>
        </div>
      </div>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="status-container">
      <div class="loader"></div>
      <p>Loading product information...</p>
    </div>
    
    <div v-else-if="error" class="status-container error">
      <i class="fas fa-exclamation-circle"></i>
      <p>{{ error }}</p>
      <button class="btn-secondary" @click="$router.push('/')">
        Return to Products
      </button>
    </div>

    <!-- Form Content -->
    <form v-else class="form-container" @submit.prevent="submitForm">
      <div class="form-content">
        <!-- Search-like Input for Name -->
        <div class="form-group">
          <div class="search-input">
            <i class="fas fa-search"></i>
            <input 
              v-model="product.name" 
              required
              placeholder="Product name"
              :class="{ 'error': validationErrors.name }"
            >
          </div>
          <span class="error-message" v-if="validationErrors.name">
            {{ validationErrors.name }}
          </span>
        </div>

        <!-- Description -->
        <div class="form-group">
          <textarea 
            v-model="product.description"
            placeholder="Product description"
            rows="3"
            class="description-input"
          ></textarea>
        </div>

        <!-- Filters Row -->
        <div class="filters-row">
          <!-- Category Select -->
          <div class="filter-item">
            <select 
              v-model="product.category" 
              required
              :class="{ 'error': validationErrors.category }"
            >
              <option value="">All Categories</option>
              <option 
                v-for="category in categories" 
                :key="category.id" 
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
            <span class="error-message" v-if="validationErrors.category">
              {{ validationErrors.category }}
            </span>
          </div>

          <!-- Stock Input -->
          <div class="filter-item">
            <input 
              type="number" 
              v-model="product.stock" 
              required
              min="0"
              placeholder="Stock quantity"
              :class="{ 'error': validationErrors.stock }"
            >
            <span class="error-message" v-if="validationErrors.stock">
              {{ validationErrors.stock }}
            </span>
          </div>

          <!-- Price Input -->
          <div class="filter-item">
            <div class="price-input">
              <span class="currency">$</span>
              <input 
                type="number" 
                v-model="product.price" 
                step="0.01" 
                required
                min="0"
                placeholder="Price"
                :class="{ 'error': validationErrors.price }"
              >
            </div>
            <span class="error-message" v-if="validationErrors.price">
              {{ validationErrors.price }}
            </span>
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="$router.push('/')">
          Cancel
        </button>
        <button type="submit" class="btn-primary">
          {{ isEdit ? 'Save Changes' : 'Add New Product' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductForm',
  props: {
    id: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      product: {
        name: '',
        description: '',
        price: 0,
        stock: 0,
        category: ''
      },
      categories: [],
      loading: true,
      error: null,
      validationErrors: {}
    };
  },
  computed: {
    isEdit() {
      return this.id !== null;
    }
  },
  async created() {
    try {
      const [categoriesResponse, productResponse] = await Promise.all([
        axios.get('http://localhost:8000/api/categories/'),
        this.isEdit ? axios.get(`http://localhost:8000/api/products/${this.id}/`) : null
      ]);
      
      this.categories = categoriesResponse.data;
      
      if (this.isEdit && productResponse) {
        this.product = {
          ...productResponse.data,
          category: productResponse.data.category
        };
      }
    } catch (error) {
      this.error = 'Error loading data';
      console.error(error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    validateForm() {
      this.validationErrors = {};
      
      if (!this.product.name.trim()) {
        this.validationErrors.name = 'Name is required';
      }
      
      if (this.product.price <= 0) {
        this.validationErrors.price = 'Price must be greater than 0';
      }
      
      if (this.product.stock < 0) {
        this.validationErrors.stock = 'Stock cannot be negative';
      }
      
      if (!this.product.category) {
        this.validationErrors.category = 'Please select a category';
      }
      
      return Object.keys(this.validationErrors).length === 0;
    },
    async submitForm() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const url = this.isEdit 
          ? `http://localhost:8000/api/products/${this.id}/`
          : 'http://localhost:8000/api/products/';
        
        const method = this.isEdit ? 'put' : 'post';
        
        await axios[method](url, this.product);
        this.$router.push('/');
      } catch (error) {
        console.error(error);
        this.error = 'Error saving product';
      }
    }
  }
};
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.breadcrumb {
  margin-bottom: 2rem;
}

.breadcrumb h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.nav-link {
  color: #6366f1;
  text-decoration: none;
  padding: 0.25rem 0.75rem;
  background-color: #eef2ff;
  border-radius: 0.375rem;
}

.separator {
  color: #9ca3af;
}

.current {
  color: #6b7280;
}

.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left h2 {
  font-size: 1.875rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.subtitle {
  color: #6b7280;
  margin: 0.5rem 0 0 0;
}

.form-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-content {
  padding: 2rem;
}

.search-input {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background-color: #f9fafb;
  transition: all 0.2s;
}

.description-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background-color: #f9fafb;
  margin-bottom: 1.5rem;
  resize: vertical;
}

.filters-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.filter-item {
  position: relative;
}

.filter-item select,
.filter-item input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background-color: #f9fafb;
  color: #111827;
  transition: all 0.2s;
}

.price-input {
  position: relative;
}

.currency {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.price-input input {
  padding-left: 1.75rem;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.error {
  border-color: #ef4444 !important;
}

.error-message {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.5rem;
  display: block;
}

.form-actions {
  padding: 1.5rem 2rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #6366f1;
  color: white;
}

.btn-primary:hover {
  background-color: #4f46e5;
}

.btn-secondary {
  background-color: white;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background-color: #f9fafb;
}

.status-container {
  background: white;
  border-radius: 1rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.status-container.error {
  color: #ef4444;
}

.loader {
  border: 3px solid #e5e7eb;
  border-radius: 50%;
  border-top: 3px solid #6366f1;
  width: 2rem;
  height: 2rem;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .filters-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
  }
}
</style> 