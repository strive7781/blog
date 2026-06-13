<script setup lang="ts">
import { ref, watch } from 'vue'
import { Editor } from '@bytemd/vue-next'
import gfm from '@bytemd/plugin-gfm'
import highlight from '@bytemd/plugin-highlight'
import breaks from '@bytemd/plugin-breaks'
import frontmatter from '@bytemd/plugin-frontmatter'
import gemoji from '@bytemd/plugin-gemoji'
import mediumZoom from '@bytemd/plugin-medium-zoom'
import 'bytemd/dist/index.css'
import 'highlight.js/styles/github-dark.css'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()

const value = ref(props.modelValue)
watch(() => props.modelValue, v => { value.value = v })
watch(value, v => emit('update:modelValue', v))

const plugins = [gfm(), highlight(), breaks(), frontmatter(), gemoji(), mediumZoom()]
</script>

<template>
  <Editor
    v-model="value"
    :plugins="plugins"
    class="bytemd-full"
    placeholder="使用 Markdown 编写文章..."
  />
</template>
