<script setup lang="ts">
import { Viewer } from '@bytemd/vue-next'
import gfm from '@bytemd/plugin-gfm'
import highlight from '@bytemd/plugin-highlight'
import breaks from '@bytemd/plugin-breaks'
import mediumZoom from '@bytemd/plugin-medium-zoom'
import 'bytemd/dist/index.css'
import 'highlight.js/styles/atom-one-dark.css'

defineProps<{ value: string }>()
const plugins = [gfm(), highlight(), breaks(), mediumZoom()]
</script>

<template>
  <div class="markdown-body">
    <Viewer :value="value" :plugins="plugins" />
  </div>
</template>
