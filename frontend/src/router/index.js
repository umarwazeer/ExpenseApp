// src/router/index.js
import { createRouter, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth'

const router = createRouter({
  history: createWebHashHistory(), // 🔥 FIX HERE
  routes
})

// GLOBAL AUTH GUARD
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/auth/login')
  } else {
    next()
  }
})  

export default router
