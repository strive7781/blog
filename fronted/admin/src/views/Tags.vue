<template>
  <div>
    <el-button type="primary" @click="openDialog()" style="margin-bottom:16px">新增标签</el-button>
    <el-table :data="list" stripe>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="slug" label="Slug" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button link @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" :title="form.id ? '编辑标签' : '新增标签'" width="420px">
      <el-form label-width="70px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="Slug"><el-input v-model="form.slug" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible=false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import http from '../api'

const list = ref<any[]>([])
const visible = ref(false)
const form = reactive<any>({ id: null, name: '', slug: '' })

async function load() { list.value = await http.get('/admin/tags') }
function openDialog(row?: any) {
  Object.assign(form, row || { id: null, name: '', slug: '' })
  visible.value = true
}
async function save() {
  await http.post('/admin/tags', form)
  visible.value = false
  load()
}
async function remove(id: number) {
  await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' })
  await http.delete(`/admin/tags/${id}`)
  load()
}
onMounted(load)
</script>
