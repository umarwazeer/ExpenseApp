// src/router/routes.js

const routes = [
  // 🔹 Authentication Pages (no MainLayout)
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/Authentication/loginPage.vue'),
      },
      {
        path: 'signup',
        name: 'signup',
        // if you don't have a signup page yet, you can point this to loginPage.vue
        component: () => import('pages/Authentication/loginPage.vue'),
      },
    ],
  },

  // 🔹 Main App (after login)
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    // meta: { requiresAuth: true },
    children: [
      { path: '', name: 'home', component: () => import('pages/home.vue') },
      { path: 'report', name: 'report', component: () => import('pages/Report.vue') },
      { path: 'stats', name: 'stats', component: () => import('pages/stats.vue') },
      { path: 'table', name: 'table', component: () => import('pages/AddUser.vue') },
      { path: 'index', name: 'index', component: () => import('pages/IndexPage.vue') },
      { path: 'budget', name: 'budget', component: () => import('pages/BudgetPage.vue') },
      { path: 'ai-chat', name: 'ai-chat', component: () => import('pages/AiChat.vue') },
      {
        path: 'categories',
        name: 'categories',
        component: () => import('pages/CategoryPage.vue'),
        // meta: { requiresAuth: true }
      },
      {
        path: 'setting',
        name: 'setting',
        component: () => import('pages/SettingsPage.vue'), // 👈 complete Settings page
      },
      { path: 'account', name: 'account', component: () => import('pages/account.vue') },

    ],
  },

  // 🔹 Error Page
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes