<template>
  <div>
    <div class="toolbar">
      <el-input v-model="keyword" placeholder="搜索标题" style="width:240px" clearable @clear="load" @keyup.enter="load" />
      <el-select v-model="status" placeholder="状态" clearable style="width:120px" @change="load">
        <el-option label="草稿" :value="0" />
        <el-option label="已发布" :value="1" />
      </el-select>
      <el-button type="primary" @click="$router.push('/articles/new')">新建文章</el-button>
    </div>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="categoryName" label="分类" width="120" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'">{{ row.status === 1 ? '已发布' : '草稿' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="viewCount" label="阅读" width="80" />
      <el-table-column prop="updatedAt" label="更新时间" width="180" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/articles/${row.id}`)">编辑</el-button>
          <el-button link type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="size"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="load"
      style="margin-top:16px"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import http, { type Article, type PageResult } from '../api'

const list = ref<Article[]>([])
const loading = ref(false)
const page = ref(1)
const size = 10
const total = ref(0)
const keyword = ref('')
const status = ref<number | undefined>()

async function load() {
  loading.value = true
  try {
    const data = await http.get<any, PageResult<Article>>('/admin/articles', {
      params: { page: page.value, size, keyword: keyword.value || undefined, status: status.value }
    })
    list.value = data.records
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function remove(id: number) {
  await ElMessageBox.confirm('确定删除该文章？', '提示', { type: 'warning' })
  await http.delete(`/admin/articles/${id}`)
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { display: flex; gap: 12px; margin-bottom: 16px; align-items: center; }
</style>
