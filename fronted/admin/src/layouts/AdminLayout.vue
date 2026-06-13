<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">Blog Admin</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item index="/articles">文章管理</el-menu-item>
        <el-menu-item index="/media">媒体库</el-menu-item>
        <el-menu-item index="/categories">分类</el-menu-item>
        <el-menu-item index="/tags">标签</el-menu-item>
        <el-menu-item index="/site">站点设置</el-menu-item>
      </el-menu>
    </aside>
    <main class="main">
      <header class="header">
        <span>{{ route.meta.title || '管理后台' }}</span>
        <el-button link type="danger" @click="logout">退出</el-button>
      </header>
      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; min-height: 100vh; }
.sidebar { width: 220px; background: #1f2937; color: #fff; }
.logo { padding: 20px; font-weight: 700; font-size: 18px; border-bottom: 1px solid #374151; }
.sidebar :deep(.el-menu) { border-right: none; background: transparent; }
.sidebar :deep(.el-menu-item) { color: #d1d5db; }
.sidebar :deep(.el-menu-item.is-active) { color: #39c5bb; background: #374151; }
.main { flex: 1; display: flex; flex-direction: column; }
.header { display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; background: #fff; border-bottom: 1px solid #e5e7eb; }
.content { padding: 24px; flex: 1; }
</style>
