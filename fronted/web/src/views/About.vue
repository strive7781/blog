<template>
  <SiteLayout>
    <div class="card-widget about">
      <h2>{{ site.site_title }}</h2>
      <p>{{ site.site_description || site.site_subtitle }}</p>
      <img v-if="site.avatar_url" :src="site.avatar_url" class="avatar" />
    </div>
  </SiteLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SiteLayout from '../layouts/SiteLayout.vue'
import { getSite } from '../api'

const site = ref<Record<string, string>>({})
onMounted(async () => { site.value = await getSite() })
</script>

<style scoped>
.about { text-align: center; padding: 32px; }
.avatar { width: 120px; height: 120px; border-radius: 50%; margin-top: 16px; }
</style>
