import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('../views/Login.vue') },
    {
      path: '/',
      component: () => import('../layouts/AdminLayout.vue'),
      redirect: '/articles',
      children: [
        { path: 'articles', component: () => import('../views/ArticleList.vue') },
        { path: 'articles/new', component: () => import('../views/ArticleEdit.vue') },
        { path: 'articles/:id', component: () => import('../views/ArticleEdit.vue') },
        { path: 'media', component: () => import('../views/Media.vue') },
        { path: 'categories', component: () => import('../views/Categories.vue') },
        { path: 'tags', component: () => import('../views/Tags.vue') },
        { path: 'site', component: () => import('../views/SiteSettings.vue') }
      ]
    }
  ]
})

router.beforeEach((to) => {
  if (to.path !== '/login' && !localStorage.getItem('token')) {
    return '/login'
  }
})

export default router
