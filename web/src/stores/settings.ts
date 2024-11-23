import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Settings } from '../types'
import { getSettings, updateSettings } from '../api/settings'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<Settings>({
    emailNotification: true,
    browserNotification: false,
    publicHistory: false,
    publicFavorites: false,
    theme: 'light'
  })

  const loading = ref(false)

  async function fetchSettings() {
    if (loading.value) return
    loading.value = true
    try {
      const data = await getSettings()
      settings.value = data
      applyTheme(data.theme)
    } catch (error) {
      console.error('获取设置失败:', error)
    } finally {
      loading.value = false
    }
  }

  async function saveSettings(newSettings: Partial<Settings>) {
    if (loading.value) return
    loading.value = true
    try {
      const data = await updateSettings(newSettings)
      settings.value = data
      applyTheme(data.theme)
      return true
    } catch (error) {
      console.error('保存设置失败:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  function applyTheme(theme: 'light' | 'dark' | 'auto') {
    const root = document.documentElement
    if (theme === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      root.classList.toggle('dark', prefersDark)
    } else {
      root.classList.toggle('dark', theme === 'dark')
    }
  }

  return {
    settings,
    loading,
    fetchSettings,
    saveSettings
  }
}) 