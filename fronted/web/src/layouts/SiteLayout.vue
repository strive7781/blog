<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getSite } from '../api'

const route = useRoute()
const site = ref<Record<string, string>>({})

onMounted(async () => {
  site.value = await getSite()
  document.documentElement.style.setProperty('--theme-color', site.value.theme_color || 'rgb(57, 197, 187)')
})

defineExpose({ site })
</script>

<template>
  <div class="site">
    <div id="web_bg" :style="{ backgroundImage: site.background_url ? `url(${site.background_url})` : undefined }"></div>
    <header id="page-header" class="not-home-page">
      <nav id="nav">
        <div class="nav-left">
          <router-link to="/" class="site-name">{{ site.site_title || "Kyle's Blog" }}</router-link>
        </div>
        <div class="nav-center">
          <router-link to="/" class="site-page">首页</router-link>
          <router-link to="/archives" class="site-page">归档</router-link>
          <router-link to="/categories" class="site-page">分类</router-link>
          <router-link to="/tags" class="site-page">标签</router-link>
          <router-link to="/about" class="site-page">关于</router-link>
        </div>
      </nav>
      <div id="page-site-info">
        <h1 id="page-title">{{ route.meta.title || site.site_title }}</h1>
      </div>
    </header>
    <main id="content-inner" class="layout">
      <div class="main-content">
        <slot />
      </div>
      <aside id="aside-content">
        <div class="card-widget card-info">
          <div class="card-content">
            <div class="avatar-img">
              <img :src="site.avatar_url" alt="avatar" />
            </div>
            <div class="author-info-name">{{ site.site_title }}</div>
            <div class="author-info-description">{{ site.site_subtitle }}</div>
          </div>
        </div>
        <div class="card-widget" v-if="site.notice_html">
          <div class="item-headline"><i class="fas fa-bullhorn"></i><span>公告栏</span></div>
          <div class="notice" v-html="site.notice_html"></div>
        </div>
      </aside>
    </main>
    <footer id="footer">
      <div class="footer-content">{{ site.footer_text }}</div>
    </footer>
  </div>
</template>

<style scoped>
.site { min-height: 100vh; position: relative; }
#web_bg {
  position: fixed; inset: 0; z-index: -1;
  background-size: cover; background-position: center;
  background-image: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg);
}
#nav {
  position: fixed; top: 0; width: 100%; z-index: 100;
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 24px; height: 60px;
  background: rgba(253, 253, 253, 0.92);
  backdrop-filter: blur(12px);
}
.site-name, .site-page { color: #4c4948; text-decoration: none; margin: 0 12px; font-weight: 500; }
.site-page:hover, .site-name:hover { color: var(--theme-color); }
.nav-center { display: flex; }
#page-header.not-home-page { padding-top: 60px; height: 280px; display: flex; align-items: center; justify-content: center; }
#page-site-info { text-align: center; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.4); }
#page-title { font-size: 2rem; margin: 0; }
#content-inner.layout { max-width: 1200px; margin: -40px auto 40px; padding: 0 16px; display: grid; grid-template-columns: 1fr 300px; gap: 20px; position: relative; z-index: 1; }
.main-content { min-width: 0; }
.card-widget {
  background: rgba(253, 253, 253, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 3px 8px rgba(7,17,27,.05);
}
.avatar-img img { width: 80px; height: 80px; border-radius: 50%; display: block; margin: 0 auto 12px; }
.author-info-name, .author-info-description { text-align: center; }
.item-headline { font-weight: 600; margin-bottom: 8px; }
#footer { text-align: center; padding: 24px; color: #666; }
@media (max-width: 900px) {
  #content-inner.layout { grid-template-columns: 1fr; }
  #aside-content { order: -1; }
}
</style>
