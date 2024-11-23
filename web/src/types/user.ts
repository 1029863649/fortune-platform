export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  vip_level: number
  vip_expire?: string
  settings: {
    emailNotification: boolean
    browserNotification: boolean
    publicHistory: boolean
    publicFavorites: boolean
    theme: 'light' | 'dark' | 'auto'
  }
  created_at: string
  updated_at: string
}

export interface UserSettings {
  emailNotification: boolean
  browserNotification: boolean
  publicHistory: boolean
  publicFavorites: boolean
  theme: 'light' | 'dark' | 'auto'
}

export interface UserUpdateRequest {
  email?: string
  username?: string
  settings?: Partial<UserSettings>
}

export interface PasswordChangeRequest {
  current_password: string
  new_password: string
} 