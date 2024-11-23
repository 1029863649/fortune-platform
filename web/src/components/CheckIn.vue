<template>
  <div class="bg-white shadow sm:rounded-lg overflow-hidden">
    <!-- 签到状态头部 -->
    <div class="px-6 py-4 bg-gradient-to-r from-primary-500 to-primary-600">
      <div class="flex items-center justify-between">
        <div class="text-white">
          <h3 class="text-xl font-bold">每日签到</h3>
          <p class="mt-1 text-primary-100">
            已连续签到 {{ streak }} 天
          </p>
        </div>
        <div class="text-right text-white">
          <p class="text-sm text-primary-100">今日可获得</p>
          <p class="text-2xl font-bold">+{{ nextReward }}</p>
        </div>
      </div>
    </div>

    <!-- 签到按钮 -->
    <div class="px-6 py-4">
      <button
        @click="handleCheckIn"
        class="w-full flex items-center justify-center px-4 py-3 rounded-lg text-lg font-medium transition-all duration-200"
        :class="[
          checked || loading
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-primary-500 text-white hover:bg-primary-600 hover:shadow-lg'
        ]"
        :disabled="checked || loading"
      >
        <template v-if="loading">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          签到中...
        </template>
        <template v-else-if="checked">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          已签到
        </template>
        <template v-else>
          立即签到
        </template>
      </button>
    </div>

    <!-- 签到日历 -->
    <div class="px-6 py-4 border-t border-gray-100">
      <h4 class="text-sm font-medium text-gray-500 mb-3">签到记录</h4>
      <div class="grid grid-cols-7 gap-2">
        <div
          v-for="(day, index) in last7Days"
          :key="index"
          class="aspect-square rounded-lg flex flex-col items-center justify-center text-sm"
          :class="[
            day.checked
              ? 'bg-primary-50 text-primary-600 border-2 border-primary-200'
              : 'bg-gray-50 text-gray-400 border border-gray-200'
          ]"
        >
          <span class="font-medium">{{ formatDay(day.date) }}</span>
          <span v-if="day.reward" class="text-xs mt-1" :class="{'text-primary-500': day.checked}">
            +{{ day.reward }}
          </span>
        </div>
      </div>
    </div>

    <!-- 签到统计 -->
    <div v-if="stats" class="px-6 py-4 bg-gray-50 border-t border-gray-100">
      <div class="grid grid-cols-3 gap-4">
        <div class="text-center">
          <p class="text-sm text-gray-500">总签到</p>
          <p class="mt-1 text-xl font-semibold text-gray-900">{{ stats.total_days }}天</p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-500">最长连续</p>
          <p class="mt-1 text-xl font-semibold text-gray-900">{{ stats.max_streak }}天</p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-500">累计获得</p>
          <p class="mt-1 text-xl font-semibold text-gray-900">{{ stats.total_rewards }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCheckInStore } from '../stores/checkin'
import { storeToRefs } from 'pinia'
import { formatDate } from '../utils/common'

const checkInStore = useCheckInStore()
const { streak, checked, loading, last7Days, stats, nextReward } = storeToRefs(checkInStore)

function formatDay(dateStr: string): string {
  return formatDate(dateStr, 'DD')
}

async function handleCheckIn() {
  if (checked.value || loading.value) return
  
  const success = await checkInStore.doCheckIn()
  if (!success) {
    // 使用项目的通知组件
    window.$message?.error('签到失败，请稍后重试')
  }
}

onMounted(async () => {
  await Promise.all([
    checkInStore.loadData(),
    checkInStore.loadStats()
  ])
})
</script> 