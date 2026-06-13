import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('../views/Home.vue'), meta: { title: '首页' } },
    { path: '/archives', component: () => import('../views/Archives.vue'), meta: { title: '归档' } },
    { path: '/post/:slug', component: () => import('../views/Post.vue'), meta: { title: '文章' } },
    { path: '/categories', component: () => import('../views/Categories.vue'), meta: { title: '分类' } },
    { path: '/tags', component: () => import('../views/Tags.vue'), meta: { title: '标签' } },
    { path: '/about', component: () => import('../views/About.vue'), meta: { title: '关于我' } }
  ],
  scrollBehavior: () => ({ top: 0 })
})

export default router
