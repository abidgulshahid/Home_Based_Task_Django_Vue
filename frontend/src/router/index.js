import { createRouter, createWebHistory } from 'vue-router'
import ProductList from '../components/ProductList.vue'
import ProductForm from '../components/ProductForm.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ProductList
  },
  {
    path: '/products/create',
    name: 'create-product',
    component: ProductForm
  },
  {
    path: '/products/:id/edit',
    name: 'edit-product',
    component: ProductForm,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 