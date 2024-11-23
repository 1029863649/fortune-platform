import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CheckInState, CheckInStats, CheckInHistory } from '../types/checkin'
import { checkIn, getCheckInStatus, getCheckInHistory, getCheckInStats } from '../api/checkin'

export const useCheckInStore = defineStore('checkin', () => {
  // 状态定义
  const streak = ref(0)
  const checked = ref(false)
  const loading = ref(false)
  const last7Days = ref<CheckInHistory[]>([])
  const stats = ref<CheckInStats | null>(null)
  const nextReward = ref(0)

  // 执行签到
  async function doCheckIn(): Promise<boolean> {
    if (checked.value || loading.value) return false
    
    loading.value = true
    try {
      const result = await checkIn()
      if (result.success) {
        checked.value = true
        streak.value = result.streak
        // 重新加载数据
        await Promise.all([loadData(), loadStats()])
        return true
      }
      return false
    } catch (error) {
      console.error('签到失败:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // 加载签到数据
  async function loadData() {
    try {
      const [statusData, historyData] = await Promise.all([
        getCheckInStatus(),
        getCheckInHistory(7)
      ])
      
      streak.value = statusData.streak
      checked.value = statusData.checked
      nextReward.value = statusData.next_reward
      last7Days.value = historyData
    } catch (error) {
      console.error('加载签到数据失败:', error)
    }
  }

  // 加载统计数据
  async function loadStats() {
    try {
      stats.value = await getCheckInStats()
    } catch (error) {
      console.error('加载签到统计失败:', error)
    }
  }

  // 重置状态
  function reset() {
    streak.value = 0
    checked.value = false
    loading.value = false
    last7Days.value = []
    stats.value = null
    nextReward.value = 0
  }

  return {
    // 状态
    streak,
    checked,
    loading,
    last7Days,
    stats,
    nextReward,
    
    // 方法
    doCheckIn,
    loadData,
    loadStats,
    reset
  }
}) 