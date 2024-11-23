import http from '../utils/http'
import type { User } from '../types'

interface LoginCredentials {
  username: string
  password: string
}

interface RegisterData {
  email: string
  username: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

interface PasswordChangeData {
  current_password: string
  new_password: string
}

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const response = await http.post<LoginResponse>('/auth/login', credentials)
  return response
}

export async function register(data: RegisterData): Promise<User> {
  const response = await http.post<User>('/auth/register', data)
  return response
}

export async function getUserInfo(): Promise<User> {
  const response = await http.get<User>('/users/me')
  return response
}

export async function updateUserInfo(data: Partial<User>): Promise<User> {
  const response = await http.put<User>('/users/me', data)
  return response
}

export async function changePassword(data: PasswordChangeData): Promise<{ message: string }> {
  const response = await http.post<{ message: string }>('/users/me/password', data)
  return response
} 