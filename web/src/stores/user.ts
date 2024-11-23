import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '../types'
import { login as loginApi, register as registerApi, getUserInfo } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  async function login(credentials: { username: string; password: string }) {
    const data = await loginApi(credentials)
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchUserInfo()
  }

  async function register(userData: {
    email: string
    username: string
    password: string
  }) {
    const data = await registerApi(userData)
    return data
  }

  async function fetchUserInfo() {
    if (token.value) {
      const data = await getUserInfo()
      user.value = data
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    login,
    register,
    logout,
    fetchUserInfo,
  }
}) 