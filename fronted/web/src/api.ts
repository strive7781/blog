import axios from 'axios'

const http = axios.create({ baseURL: '/api', timeout: 20000 })

http.interceptors.response.use((res) => {
  const data = res.data
  if (data.code !== 200) return Promise.reject(data)
  return data.data
})

export default http

export interface Article {
  id: number
  title: string
  slug: string
  summary?: string
  contentMd?: string
  coverUrl?: string
  categoryId?: number
  categoryName?: string
  status: number
  viewCount: number
  publishedAt?: string
  tags?: { id: number; name: string; slug: string }[]
}

export interface PageResult<T> {
  total: number
  page: number
  size: number
  records: T[]
}

export async function getSite() {
  return http.get<any, Record<string, string>>('/public/site')
}

export async function getArticles(page = 1, size = 10, categoryId?: number) {
  return http.get<any, PageResult<Article>>('/public/articles', { params: { page, size, categoryId } })
}

export async function getArticle(slug: string) {
  return http.get<any, Article>(`/public/articles/${slug}`)
}

export async function getCategories() {
  return http.get<any, any[]>('/public/categories')
}

export async function getTags() {
  return http.get<any, any[]>('/public/tags')
}
