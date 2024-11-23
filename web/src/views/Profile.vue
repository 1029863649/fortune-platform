<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- 签到组件 -->
    <CheckIn />
    
    <!-- 个人信息卡片 -->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">个人信息</h3>
        
        <!-- 基本信息表单 -->
        <form @submit.prevent="updateProfile" class="mt-6">
          <div class="space-y-6">
            <!-- 用户名 -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
              <div class="mt-1">
                <input
                  id="username"
                  v-model="formData.username"
                  type="text"
                  class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- 邮箱 -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">邮箱</label>
              <div class="mt-1">
                <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- 提交按钮 -->
            <div>
              <button
                type="submit"
                class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                :disabled="loading"
              >
                {{ loading ? '更新中...' : '更新信息' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 修改密码卡片 -->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">修改密码</h3>
        <form @submit.prevent="changePassword" class="mt-6">
          <div class="space-y-6">
            <!-- 当前密码 -->
            <div>
              <label for="currentPassword" class="block text-sm font-medium text-gray-700">当前密码</label>
              <div class="mt-1">
                <input
                  id="currentPassword"
                  v-model="passwordData.currentPassword"
                  type="password"
                  class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  :disabled="passwordLoading"
                />
              </div>
            </div>

            <!-- 新密码 -->
            <div>
              <label for="newPassword" class="block text-sm font-medium text-gray-700">新密码</label>
              <div class="mt-1">
                <input
                  id="newPassword"
                  v-model="passwordData.newPassword"
                  type="password"
                  class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  :disabled="passwordLoading"
                />
              </div>
            </div>

            <!-- 确认新密码 -->
            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700">确认新密码</label>
              <div class="mt-1">
                <input
                  id="confirmPassword"
                  v-model="passwordData.confirmPassword"
                  type="password"
                  class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  :disabled="passwordLoading"
                />
              </div>
            </div>

            <!-- 提交按钮 -->
            <div>
              <button
                type="submit"
                class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                :disabled="passwordLoading"
              >
                {{ passwordLoading ? '修改中...' : '修改密码' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 会员信息卡片 -->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">会员信息</h3>
        <div class="mt-6 space-y-4">
          <!-- 会员等级 -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">会员等级</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {{ getVipLevelName(user?.vip_level || 0) }}
            </dd>
          </div>
          
          <!-- 到期时间 -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">到期时间</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {{ user?.vip_expire ? formatDate(user.vip_expire) : '无会员' }}
            </dd>
          </div>
          
          <!-- 剩余次数 -->
          <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">今日剩余次数</dt>
            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {{ quota.remaining }}/{{ quota.daily_limit }}
              <span class="ml-2 text-gray-500">
                重置时间: {{ formatDate(quota.reset_time) }}
              </span>
            </dd>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { storeToRefs } from 'pinia'
import { updateUserInfo, changePassword as changePasswordApi } from '../api/auth'
import { getQuota } from '../api/quota'
import { formatDate } from '../utils/common'
import type { User, Quota } from '../types'
import CheckIn from '../components/CheckIn.vue'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const loading = ref(false)
const passwordLoading = ref(false)

const formData = ref({
  username: '',
  email: ''
})

const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const quota = ref<Quota>({
  daily_limit: 0,
  used_today: 0,
  remaining: 0,
  reset_time: new Date().toISOString()
})

function getVipLevelName(level: number): string {
  const levels = {
    0: '普通用户',
    1: '青铜会员',
    2: '白银会员',
    3: '黄金会员',
    4: '铂金会员',
    5: '钻石会员'
  }
  return levels[level as keyof typeof levels] || '未知等级'
}

async function updateProfile() {
  if (loading.value) return
  loading.value = true
  try {
    const updatedUser = await updateUserInfo(formData.value)
    userStore.$patch({ user: updatedUser })
    alert('更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    alert('更新失败')
  } finally {
    loading.value = false
  }
}

async function changePassword() {
  if (passwordLoading.value) return
  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  passwordLoading.value = true
  try {
    await changePasswordApi({
      current_password: passwordData.value.currentPassword,
      new_password: passwordData.value.newPassword
    })
    alert('密码修改成功')
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    alert('密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

async function loadQuota() {
  try {
    quota.value = await getQuota()
  } catch (error) {
    console.error('获取配额信息失败:', error)
  }
}

onMounted(async () => {
  if (user.value) {
    formData.value.username = user.value.username
    formData.value.email = user.value.email
  }
  await loadQuota()
})
</script> 