<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">数据统计</h3>
        
        <!-- 总体统计 -->
        <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-4">
          <div class="bg-gray-50 px-4 py-5 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">总占卜次数</dt>
            <dd class="mt-1 text-3xl font-semibold text-gray-900">
              {{ stats.total_divinations }}
            </dd>
          </div>
          <div class="bg-gray-50 px-4 py-5 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">收藏数量</dt>
            <dd class="mt-1 text-3xl font-semibold text-gray-900">
              {{ stats.favorites_count }}
            </dd>
          </div>
          <div class="bg-gray-50 px-4 py-5 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">连续签到</dt>
            <dd class="mt-1 text-3xl font-semibold text-gray-900">
              {{ checkinStreak }}天
            </dd>
          </div>
          <div class="bg-gray-50 px-4 py-5 rounded-lg">
            <dt class="text-sm font-medium text-gray-500">剩余次数</dt>
            <dd class="mt-1 text-3xl font-semibold text-gray-900">
              {{ quota.remaining }}
            </dd>
          </div>
        </div>

        <!-- 占卜类型统计 -->
        <div class="mt-10">
          <h4 class="text-lg font-medium text-gray-900">占卜类型分布</h4>
          <div class="mt-4">
            <div v-for="(count, type) in stats.type_stats" :key="type" class="mt-4">
              <div class="flex items-center justify-between">
                <div class="text-sm font-medium text-gray-500">
                  {{ getDivinationType(type) }}
                </div>
                <div class="text-sm font-medium text-gray-900">{{ count }}</div>
              </div>
              <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-primary-600 h-2 rounded-full"
                  :style="{
                    width: `${(count / stats.total_divinations) * 100}%`
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 趋势图表 -->
        <div class="mt-10">
          <h4 class="text-lg font-medium text-gray-900">占卜趋势</h4>
          <div class="mt-4 h-64">
            <canvas ref="trendChart"></canvas>
          </div>
        </div>

        <!-- 签到日历 -->
        <div class="mt-10">
          <h4 class="text-lg font-medium text-gray-900">签到记录</h4>
          <div class="mt-4 grid grid-cols-7 gap-2">
            <div v-for="day in last30Days" :key="day.date" 
                 class="aspect-square rounded-lg flex items-center justify-center"
                 :class="[
                   day.checked 
                     ? 'bg-primary-100 text-primary-700' 
                     : 'bg-gray-50 text-gray-500'
                 ]"
            >
              {{ formatDay(day.date) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserStats, getTrendData } from '../api/stats'
import { getQuota } from '../api/quota'
import { getStreak, getCheckInHistory } from '../api/checkin'
import { formatDate } from '../utils/common'
import type { Stats, Quota } from '../types'
import Chart from 'chart.js/auto'

const stats = ref<Stats>({
  total_divinations: 0,
  type_stats: {
    answer_book: 0,
    tarot: 0,
    yijing: 0
  },
  favorites_count: 0
})

const quota = ref<Quota>({
  daily_limit: 0,
  used_today: 0,
  remaining: 0,
  reset_time: new Date().toISOString()
})

const checkinStreak = ref(0)
const last30Days = ref<Array<{date: string; checked: boolean}>>([])

const trendChart = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

const divinationTypes = {
  answer_book: '答案之书',
  tarot: '塔罗牌',
  yijing: '易经'
}

function getDivinationType(type: string) {
  return divinationTypes[type as keyof typeof divinationTypes] || type
}

function formatDay(date: string) {
  return new Date(date).getDate()
}

async function loadStats() {
  try {
    const [statsData, quotaData, trendData, streakData, historyData] = await Promise.all([
      getUserStats(),
      getQuota(),
      getTrendData(7),
      getStreak(),
      getCheckInHistory(30)
    ])
    
    stats.value = statsData
    quota.value = quotaData
    checkinStreak.value = streakData.streak
    last30Days.value = historyData
    
    if (trendChart.value && trendData) {
      chart = new Chart(trendChart.value, {
        type: 'line',
        data: {
          labels: trendData.dates,
          datasets: [{
            label: '占卜次数',
            data: trendData.counts,
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(async () => {
  await loadStats()
})
</script> 