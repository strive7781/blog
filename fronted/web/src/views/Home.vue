<template>
  <div class="home">
    <div class="hero" :style="{ backgroundImage: site.background_url ? `url(${site.background_url})` : undefined }">
      <nav class="hero-nav">
        <router-link to="/" class="brand">{{ site.site_title || "Kyle's Blog" }}</router-link>
        <div class="links">
          <router-link to="/">首页</router-link>
          <router-link to="/archives">归档</router-link>
          <router-link to="/categories">分类</router-link>
          <router-link to="/tags">标签</router-link>
          <router-link to="/about">关于</router-link>
        </div>
      </nav>
      <div class="hero-text">
        <h1>{{ site.site_title || "Kyle's Blog" }}</h1>
        <p>{{ site.site_subtitle }}</p>
      </div>
    </div>
    <div class="home-layout">
      <div class="posts">
        <article v-for="post in posts" :key="post.id" class="post-card" @click="$router.push(`/post/${post.slug}`)">
          <img v-if="post.coverUrl" :src="post.coverUrl" class="cover" />
          <div class="body">
            <h2>{{ post.title }}</h2>
            <p class="summary">{{ post.summary }}</p>
            <div class="meta">
              <span>{{ formatDate(post.publishedAt) }}</span>
              <span v-if="post.categoryName">{{ post.categoryName }}</span>
              <span v-for="t in post.tags" :key="t.id" class="tag">{{ t.name }}</span>
            </div>
          </div>
        </article>
        <div class="pager" v-if="total > size">
          <button :disabled="page<=1" @click="load(page-1)">上一页</button>
          <span>{{ page }} / {{ Math.ceil(total/size) }}</span>
          <button :disabled="page*size>=total" @click="load(page+1)">下一页</button>
        </div>
      </div>
      <aside class="sidebar">
        <div class="card-widget card-info">
          <img :src="site.avatar_url" class="avatar" />
          <h3>{{ site.site_title }}</h3>
          <p>{{ site.site_subtitle }}</p>
        </div>
        <div class="card-widget" v-if="site.notice_html">
          <h4><i class="fas fa-bullhorn"></i> 公告栏</h4>
          <div v-html="site.notice_html"></div>
        </div>
      </aside>
    </div>
    <footer>{{ site.footer_text }}</footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getArticles, getSite, type Article } from '../api'

const site = ref<Record<string, string>>({})
const posts = ref<Article[]>([])
const page = ref(1)
const size = 10
const total = ref(0)

function formatDate(d?: string) {
  if (!d) return ''
  return d.replace('T', ' ').slice(0, 10)
}

async function load(p = 1) {
  page.value = p
  const data = await getArticles(p, size)
  posts.value = data.records
  total.value = data.total
}

onMounted(async () => {
  site.value = await getSite()
  document.documentElement.style.setProperty('--theme-color', site.value.theme_color || 'rgb(57, 197, 187)')
  await load()
})
</script>

<style scoped>
.home { min-height: 100vh; }
.hero {
  height: 100vh; background-size: cover; background-position: center; position: relative;
  display: flex; flex-direction: column; color: #fff;
}
.hero-nav {
  display: flex; justify-content: space-between; align-items: center; padding: 16px 32px;
  background: rgba(255,255,255,.15); backdrop-filter: blur(8px);
}
.brand, .links a { color: #fff; text-decoration: none; margin-left: 16px; font-weight: 500; }
.hero-text { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-shadow: 0 2px 12px rgba(0,0,0,.35); }
.hero-text h1 { font-size: 3rem; margin: 0 0 12px; }
.home-layout {
  max-width: 1200px; margin: -80px auto 40px; padding: 0 16px;
  display: grid; grid-template-columns: 1fr 300px; gap: 20px; position: relative; z-index: 2;
}
.post-card {
  display: grid; grid-template-columns: 220px 1fr; gap: 16px;
  background: rgba(253,253,253,.95); backdrop-filter: blur(12px);
  border-radius: 12px; overflow: hidden; margin-bottom: 16px; cursor: pointer;
  box-shadow: 0 3px 8px rgba(7,17,27,.05); transition: transform .2s, box-shadow .2s;
}
.post-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(7,17,27,.1); }
.cover { width: 100%; height: 100%; min-height: 140px; object-fit: cover; }
.body { padding: 16px 16px 16px 0; }
.body h2 { margin: 0 0 8px; font-size: 1.25rem; color: #1f2d3d; }
.summary { color: #666; margin: 0 0 12px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.meta { font-size: 13px; color: #999; display: flex; gap: 8px; flex-wrap: wrap; }
.tag { background: rgba(57,197,187,.15); color: var(--theme-color); padding: 2px 8px; border-radius: 4px; }
.card-widget { background: rgba(253,253,253,.95); backdrop-filter: blur(12px); border-radius: 12px; padding: 16px; margin-bottom: 16px; }
.avatar { width: 80px; height: 80px; border-radius: 50%; display: block; margin: 0 auto 12px; }
.card-info h3, .card-info p { text-align: center; margin: 4px 0; }
.pager { display: flex; justify-content: center; gap: 16px; align-items: center; padding: 16px; }
.pager button { padding: 8px 16px; border: 1px solid var(--theme-color); background: #fff; color: var(--theme-color); border-radius: 6px; cursor: pointer; }
footer { text-align: center; padding: 24px; color: #888; }
@media (max-width: 900px) {
  .home-layout { grid-template-columns: 1fr; margin-top: -40px; }
  .post-card { grid-template-columns: 1fr; }
  .cover { height: 180px; }
  .body { padding: 16px; }
}
</style>
