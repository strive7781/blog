<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2>博客管理后台</h2>
      <el-form @submit.prevent="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="admin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="admin123" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: 'admin', password: 'admin123' })

async function submit() {
  loading.value = true
  try {
    const data = await http.post<any, { token: string }>('/auth/login', form)
    localStorage.setItem('token', data.token)
    router.push('/articles')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.login-card { width: 380px; }
h2 { text-align: center; margin: 0 0 24px; }
</style>
