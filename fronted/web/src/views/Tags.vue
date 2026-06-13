<template>
  <SiteLayout>
    <div class="card-widget tags">
      <router-link v-for="t in tags" :key="t.id" :to="`/?tag=${t.slug}`" class="tag">{{ t.name }}</router-link>
    </div>
  </SiteLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SiteLayout from '../layouts/SiteLayout.vue'
import { getTags } from '../api'

const tags = ref<any[]>([])
onMounted(async () => { tags.value = await getTags() })
</script>

<style scoped>
.tags { display: flex; flex-wrap: wrap; gap: 10px; }
.tag { background: rgba(57,197,187,.15); color: var(--theme-color); padding: 6px 14px; border-radius: 20px; }
</style>
