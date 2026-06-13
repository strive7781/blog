<template>
  <SiteLayout>
    <div class="card-widget">
      <div v-for="post in posts" :key="post.id" class="item">
        <span class="date">{{ formatDate(post.publishedAt) }}</span>
        <router-link :to="`/post/${post.slug}`">{{ post.title }}</router-link>
      </div>
      <div class="pager" v-if="total > size">
        <button :disabled="page<=1" @click="load(page-1)">上一页</button>
        <span>{{ page }}</span>
        <button :disabled="page*size>=total" @click="load(page+1)">下一页</button>
      </div>
    </div>
  </SiteLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SiteLayout from '../layouts/SiteLayout.vue'
import { getArticles, type Article } from '../api'

const posts = ref<Article[]>([])
const page = ref(1)
const size = 20
const total = ref(0)

function formatDate(d?: string) { return d?.slice(0, 10) || '' }

async function load(p = 1) {
  page.value = p
  const data = await getArticles(p, size)
  posts.value = data.records
  total.value = data.total
}

onMounted(() => load())
</script>

<style scoped>
.item { padding: 12px 0; border-bottom: 1px dashed #eee; display: flex; gap: 16px; }
.date { color: #999; min-width: 100px; }
.pager { display: flex; justify-content: center; gap: 12px; margin-top: 16px; }
</style>
