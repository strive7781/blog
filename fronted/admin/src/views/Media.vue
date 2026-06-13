<template>
  <div>
    <el-upload drag :show-file-list="false" :http-request="upload" accept="image/*" multiple>
      <div>拖拽或点击上传图片</div>
    </el-upload>
    <div class="grid" v-loading="loading">
      <div v-for="item in list" :key="item.id" class="item">
        <img :src="item.url" :alt="item.filename" />
        <div class="meta">
          <span>{{ item.filename }}</span>
          <div>
            <el-button link type="primary" @click="copy(item.url)">复制链接</el-button>
            <el-button link type="danger" @click="remove(item.id)">删除</el-button>
          </div>
        </div>
      </div>
    </div>
    <el-pagination v-model:current-page="page" :total="total" :page-size="20" layout="total, prev, pager, next" @current-change="load" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import http, { type PageResult } from '../api'

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function load() {
  loading.value = true
  try {
    const data = await http.get<any, PageResult<any>>('/admin/media', { params: { page: page.value, size: 20 } })
    list.value = data.records
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function upload(options: any) {
  const fd = new FormData()
  fd.append('file', options.file)
  await http.post('/admin/media/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  ElMessage.success('上传成功')
  load()
}

function copy(url: string) {
  navigator.clipboard.writeText(location.origin + url)
  ElMessage.success('已复制')
}

async function remove(id: number) {
  await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' })
  await http.delete(`/admin/media/${id}`)
  load()
}

onMounted(load)
</script>

<style scoped>
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin: 20px 0; }
.item { background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.item img { width: 100%; height: 140px; object-fit: cover; }
.meta { padding: 8px; font-size: 12px; }
.meta span { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-bottom: 4px; }
</style>
