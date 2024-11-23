export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  vip_level: number
  vip_expire?: string
  created_at: string
  updated_at: string
}

export interface DivinationRecord {
  id: string
  user_id: string
  type: 'answer_book' | 'tarot' | 'yijing'
  question: string
  answer: string
  created_at: string
  updated_at: string
}

export interface Favorite {
  id: string
  user_id: string
  record_id: string
  created_at: string
  updated_at: string
  record?: DivinationRecord
}

export interface Quota {
  daily_limit: number
  used_today: number
  remaining: number
  reset_time: string
}

export interface Stats {
  total_divinations: number
  type_stats: {
    answer_book: number
    tarot: number
    yijing: number
  }
  favorites_count: number
}

export interface TrendData {
  dates: string[]
  counts: number[]
}

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface RouteMeta {
  requiresAuth?: boolean
  title?: string
}

export interface HttpConfig {
  headers?: Record<string, string>
  params?: Record<string, any>
}

export interface PaginationParams {
  skip?: number
  limit?: number
}

export interface PaginatedResponse<T> {
  total: number
  items: T[]
}

export interface Settings {
  emailNotification: boolean
  browserNotification: boolean
  publicHistory: boolean
  publicFavorites: boolean
  theme: 'light' | 'dark' | 'auto'
} 