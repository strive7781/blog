<template>
  <el-form v-loading="loading" label-width="100px" style="max-width:720px;background:#fff;padding:24px;border-radius:8px">
    <el-form-item label="站点标题"><el-input v-model="form.site_title" /></el-form-item>
    <el-form-item label="副标题"><el-input v-model="form.site_subtitle" /></el-form-item>
    <el-form-item label="站点描述"><el-input v-model="form.site_description" type="textarea" /></el-form-item>
    <el-form-item label="头像 URL"><el-input v-model="form.avatar_url" /></el-form-item>
    <el-form-item label="背景图 URL"><el-input v-model="form.background_url" /></el-form-item>
    <el-form-item label="主题色"><el-input v-model="form.theme_color" placeholder="rgb(57, 197, 187)" /></el-form-item>
    <el-form-item label="页脚文字"><el-input v-model="form.footer_text" /></el-form-item>
    <el-form-item label="公告栏"><el-input v-model="form.notice_html" type="textarea" :rows="4" /></el-form-item>
    <el-button type="primary" :loading="saving" @click="save">保存设置</el-button>
  </el-form>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import http from '../api'

const loading = ref(false)
const saving = ref(false)
const form = reactive<Record<string, string>>({
  site_title: '', site_subtitle: '', site_description: '',
  avatar_url: '', background_url: '', theme_color: '', footer_text: '', notice_html: ''
})

async function load() {
  loading.value = true
  try {
    const data = await http.get<any, Record<string, string>>('/admin/site')
    Object.assign(form, data)
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    await http.put('/admin/site', form)
    ElMessage.success('保存成功')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
