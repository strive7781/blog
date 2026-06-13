<template>
  <SiteLayout>
    <div class="card-widget">
      <div v-for="c in categories" :key="c.id" class="item">
        <router-link :to="`/?category=${c.id}`">{{ c.name }}</router-link>
        <span class="desc">{{ c.description }}</span>
      </div>
    </div>
  </SiteLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SiteLayout from '../layouts/SiteLayout.vue'
import { getCategories } from '../api'

const categories = ref<any[]>([])
onMounted(async () => { categories.value = await getCategories() })
</script>

<style scoped>
.item { padding: 12px 0; border-bottom: 1px dashed #eee; display: flex; justify-content: space-between; }
.desc { color: #999; font-size: 14px; }
</style>
