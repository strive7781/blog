<template>
  <SiteLayout>
    <article class="post-card" v-if="article">
      <h1 class="title">{{ article.title }}</h1>
      <div class="meta">
        <span><i class="far fa-calendar"></i> {{ formatDate(article.publishedAt) }}</span>
        <span v-if="article.categoryName"><i class="far fa-folder-open"></i> {{ article.categoryName }}</span>
        <span><i class="far fa-eye"></i> {{ article.viewCount }}</span>
        <router-link v-for="t in article.tags" :key="t.id" :to="`/tags#${t.slug}`" class="tag">{{ t.name }}</router-link>
      </div>
      <img v-if="article.coverUrl" :src="article.coverUrl" class="cover" />
      <MarkdownViewer :value="article.contentMd || ''" />
    </article>
  </SiteLayout>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import SiteLayout from '../layouts/SiteLayout.vue'
import MarkdownViewer from '../components/MarkdownViewer.vue'
import { getArticle, type Article } from '../api'

const route = useRoute()
const article = ref<Article | null>(null)

function formatDate(d?: string) {
  return d ? d.replace('T', ' ').slice(0, 16) : ''
}

async function load() {
  article.value = await getArticle(route.params.slug as string)
  document.title = `${article.value.title} | Kyle's Blog`
}

onMounted(load)
watch(() => route.params.slug, load)
</script>

<style scoped>
.post-card {
  background: rgba(253,253,253,.95);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 3px 8px rgba(7,17,27,.05);
}
.title { margin: 0 0 16px; font-size: 2rem; color: #1f2d3d; text-align: center; }
.meta { text-align: center; color: #999; font-size: 14px; margin-bottom: 24px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.tag { background: rgba(57,197,187,.15); color: var(--theme-color); padding: 2px 10px; border-radius: 4px; }
.cover { width: 100%; max-height: 360px; object-fit: cover; border-radius: 8px; margin-bottom: 24px; }
</style>
