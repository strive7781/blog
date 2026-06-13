<template>
  <div v-loading="loading">
    <el-form label-width="80px" class="meta-form">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="标题" required>
            <el-input v-model="form.title" placeholder="文章标题" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="Slug">
            <el-input v-model="form.slug" placeholder="留空自动生成" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="分类">
            <el-select v-model="form.categoryId" placeholder="选择分类" clearable style="width:100%">
              <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="标签">
            <el-select v-model="form.tagIds" multiple placeholder="选择标签" style="width:100%">
              <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <el-form-item label="摘要">
            <el-input v-model="form.summary" type="textarea" :rows="2" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="封面">
            <div class="cover-row">
              <el-input v-model="form.coverUrl" placeholder="图片 URL" />
              <el-upload :show-file-list="false" :http-request="uploadCover" accept="image/*">
                <el-button>上传</el-button>
              </el-upload>
            </div>
            <img v-if="form.coverUrl" :src="form.coverUrl" class="cover-preview" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="状态">
            <el-radio-group v-model="form.status">
              <el-radio :value="0">草稿</el-radio>
              <el-radio :value="1">发布</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <ByteMdEditor v-model="form.contentMd" />

    <div class="actions">
      <el-button @click="$router.back()">返回</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import http, { type Article } from '../api'
import ByteMdEditor from '../components/ByteMdEditor.vue'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const saving = ref(false)
const categories = ref<any[]>([])
const tags = ref<any[]>([])

const form = reactive({
  title: '',
  slug: '',
  summary: '',
  contentMd: '# 新文章\n\n在这里编写内容...',
  coverUrl: '',
  categoryId: undefined as number | undefined,
  tagIds: [] as number[],
  status: 0
})

const isEdit = !!route.params.id

async function loadMeta() {
  categories.value = await http.get('/admin/categories')
  tags.value = await http.get('/admin/tags')
}

async function loadArticle() {
  if (!isEdit) return
  loading.value = true
  try {
    const data = await http.get<any, Article>(`/admin/articles/${route.params.id}`)
    Object.assign(form, {
      title: data.title,
      slug: data.slug,
      summary: data.summary,
      contentMd: data.contentMd,
      coverUrl: data.coverUrl,
      categoryId: data.categoryId,
      tagIds: data.tags?.map(t => t.id) || [],
      status: data.status
    })
  } finally {
    loading.value = false
  }
}

async function uploadCover(options: any) {
  const fd = new FormData()
  fd.append('file', options.file)
  const media = await http.post<any, { url: string }>('/admin/media/upload', fd, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  form.coverUrl = media.url
  ElMessage.success('封面上传成功')
}

async function save() {
  if (!form.title.trim()) {
    ElMessage.warning('请填写标题')
    return
  }
  saving.value = true
  try {
    if (isEdit) {
      await http.put(`/admin/articles/${route.params.id}`, form)
    } else {
      await http.post('/admin/articles', form)
    }
    ElMessage.success('保存成功')
    router.push('/articles')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await loadMeta()
  await loadArticle()
})
</script>

<style scoped>
.meta-form { background: #fff; padding: 16px; border-radius: 8px; margin-bottom: 16px; }
.cover-row { display: flex; gap: 8px; width: 100%; }
.cover-preview { margin-top: 8px; max-width: 200px; border-radius: 6px; }
.actions { margin-top: 16px; display: flex; gap: 12px; justify-content: flex-end; }
</style>
