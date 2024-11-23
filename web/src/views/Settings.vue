<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">系统设置</h3>
        
        <!-- 通知设置 -->
        <div class="mt-6">
          <h4 class="text-base font-medium text-gray-900">通知设置</h4>
          <div class="mt-4 space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">邮件通知</label>
                <p class="text-sm text-gray-500">接收重要的系统通知和提醒</p>
              </div>
              <button
                @click="toggleEmailNotification"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.emailNotification ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.emailNotification ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>
            
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">浏览器通知</label>
                <p class="text-sm text-gray-500">在浏览器中接收实时提醒</p>
              </div>
              <button
                @click="toggleBrowserNotification"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.browserNotification ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.browserNotification ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>

            <!-- 签到提醒 -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">签到提醒</label>
                <p class="text-sm text-gray-500">每日签到提醒通知</p>
              </div>
              <button
                @click="toggleCheckInReminder"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.checkInReminder ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.checkInReminder ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 隐私设置 -->
        <div class="mt-10 pt-6 border-t border-gray-200">
          <h4 class="text-base font-medium text-gray-900">隐私设置</h4>
          <div class="mt-4 space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">公开历史记录</label>
                <p class="text-sm text-gray-500">允许其他用户查看您的占卜历史</p>
              </div>
              <button
                @click="togglePublicHistory"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.publicHistory ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.publicHistory ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>
            
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">公开收藏</label>
                <p class="text-sm text-gray-500">允许其他用户查看您的收藏列表</p>
              </div>
              <button
                @click="togglePublicFavorites"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.publicFavorites ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.publicFavorites ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>

            <!-- 公开签到记录 -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">公开签到记录</label>
                <p class="text-sm text-gray-500">允许其他用户查看您的签到记录</p>
              </div>
              <button
                @click="togglePublicCheckIn"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200"
                :class="[settings.publicCheckIn ? 'bg-primary-600' : 'bg-gray-200']"
              >
                <span
                  class="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                  :class="[settings.publicCheckIn ? 'translate-x-5' : 'translate-x-0']"
                ></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 主题设置 -->
        <div class="mt-10 pt-6 border-t border-gray-200">
          <h4 class="text-base font-medium text-gray-900">主题设置</h4>
          <div class="mt-4">
            <div class="grid grid-cols-3 gap-4">
              <button
                v-for="theme in themes"
                :key="theme.id"
                @click="selectTheme(theme.id)"
                class="p-4 rounded-lg border-2"
                :class="[
                  settings.theme === theme.id
                    ? 'border-primary-500 ring-2 ring-primary-500'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <div class="text-sm font-medium text-gray-900">{{ theme.name }}</div>
                <div class="mt-1 text-xs text-gray-500">{{ theme.description }}</div>
              </button>
            </div>
          </div>
        </div>

        <!-- 保存按钮 -->
        <div class="mt-10 pt-6 border-t border-gray-200">
          <button
            @click="saveSettings"
            class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="loading"
          >
            {{ loading ? '保存中...' : '保存设置' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'
import { storeToRefs } from 'pinia'

const settingsStore = useSettingsStore()
const { settings, loading } = storeToRefs(settingsStore)

const themes = [
  { id: 'light', name: '浅色主题', description: '默认的浅色主题' },
  { id: 'dark', name: '深色主题', description: '护眼的深色主题' },
  { id: 'auto', name: '自动主题', description: '跟随系统设置' },
]

function toggleEmailNotification() {
  settingsStore.saveSettings({
    emailNotification: !settings.value.emailNotification
  })
}

function toggleBrowserNotification() {
  settingsStore.saveSettings({
    browserNotification: !settings.value.browserNotification
  })
}

function toggleCheckInReminder() {
  settingsStore.saveSettings({
    checkInReminder: !settings.value.checkInReminder
  })
}

function togglePublicHistory() {
  settingsStore.saveSettings({
    publicHistory: !settings.value.publicHistory
  })
}

function togglePublicFavorites() {
  settingsStore.saveSettings({
    publicFavorites: !settings.value.publicFavorites
  })
}

function togglePublicCheckIn() {
  settingsStore.saveSettings({
    publicCheckIn: !settings.value.publicCheckIn
  })
}

function selectTheme(themeId: 'light' | 'dark' | 'auto') {
  settingsStore.saveSettings({
    theme: themeId
  })
}

onMounted(() => {
  settingsStore.fetchSettings()
})
</script> 