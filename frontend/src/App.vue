<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
</script>

<template>
  <div id="app">
    <header>
      <div class="header-content">
        <h1>E-commerce Dashboard</h1>
        <nav>
          <router-link to="/" class="nav-link">
            <i class="fas fa-box"></i> Products
          </router-link>
          <router-link to="/products/create" class="nav-link">
            <i class="fas fa-plus"></i> Create Product
          </router-link>
        </nav>
      </div>
    </header>
    <main>
      <router-view/>
    </main>
    <footer>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1a202c;
}

nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: #4a5568;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: #edf2f7;
  color: #2d3748;
}

.nav-link.router-link-active {
  background-color: #ebf4ff;
  color: #3182ce;
}

main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 20px;
  width: 100%;
  background-color: #f7fafc;
}

footer {
  background-color: #2d3748;
  color: #ffffff;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

/* Global Styles */
button {
  background-color: #4299e1;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #3182ce;
}

button.secondary {
  background-color: #718096;
}

button.secondary:hover {
  background-color: #4a5568;
}

button.danger {
  background-color: #f56565;
}

button.danger:hover {
  background-color: #e53e3e;
}

.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}
</style>
