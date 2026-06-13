import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from './router'

const http = axios.create({ baseURL: '/api', timeout: 30000 })

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data.code !== 200) {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(data)
    }
    return data.data
  },
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    ElMessage.error(err.response?.data?.message || '网络错误')
    return Promise.reject(err)
  }
)

export default http

export interface Article {
  id?: number
  title: string
  slug?: string
  summary?: string
  contentMd: string
  coverUrl?: string
  categoryId?: number
  status: number
  tagIds?: number[]
  tags?: { id: number; name: string }[]
  publishedAt?: string
}

export interface PageResult<T> {
  total: number
  page: number
  size: number
  records: T[]
}
