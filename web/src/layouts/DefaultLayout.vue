<template>
  <div class="min-h-screen bg-gray-100">
    <!-- 导航栏 -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-primary-600">天机阁</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                v-for="item in navItems"
                :key="item.path"
                :to="item.path"
                class="inline-flex items-center px-1 pt-1 border-b-2"
                :class="[
                  route.path === item.path
                    ? 'border-primary-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <div class="ml-3 relative">
              <div v-if="user" class="flex items-center space-x-4">
                <span class="text-sm text-gray-700">{{ user.username }}</span>
                <button
                  @click="logout"
                  class="text-sm text-gray-700 hover:text-gray-900"
                >
                  退出
                </button>
              </div>
              <div v-else class="flex items-center space-x-4">
                <router-link
                  to="/auth/login"
                  class="text-sm text-gray-700 hover:text-gray-900"
                >
                  登录
                </router-link>
                <router-link
                  to="/auth/register"
                  class="text-sm text-gray-700 hover:text-gray-900"
                >
                  注册
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="bg-white">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div class="text-center text-gray-500 text-sm">
          <p>&copy; 2024 天机阁. All rights reserved.</p>
          <p class="mt-1">
            <a href="https://sanshengshui.com" target="_blank" class="hover:text-gray-700">
              官网: sanshengshui.com
            </a>
            <span class="mx-2">·</span>
            <span>开发者: 仲戌字</span>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const navItems = [
  { name: '首页', path: '/' },
  { name: '占卜', path: '/divination' },
  { name: '历史', path: '/history' },
  { name: '收藏', path: '/favorites' },
  { name: '统计', path: '/stats' },
  { name: '个人中心', path: '/profile' },
  { name: '设置', path: '/settings' },
]

const logout = () => {
  userStore.logout()
  router.push('/auth/login')
}
</script> 