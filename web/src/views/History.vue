<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">占卜历史记录</h3>
        
        <!-- 记录列表 -->
        <div class="mt-6 space-y-6">
          <div v-if="loading" class="text-center py-4">
            <div class="text-gray-500">加载中...</div>
          </div>
          
          <div v-else-if="records.length === 0" class="text-center py-4">
            <div class="text-gray-500">暂无占卜记录</div>
          </div>
          
          <div v-else v-for="record in records" :key="record.id" class="bg-gray-50 p-4 rounded-lg">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-sm text-gray-500">
                  {{ formatDate(record.created_at) }}
                  <span class="mx-2">·</span>
                  {{ getDivinationType(record.type) }}
                </div>
                <div class="mt-2 text-gray-900 font-medium">{{ record.question }}</div>
                <div class="mt-2 text-gray-600 whitespace-pre-line">{{ record.answer }}</div>
              </div>
              <button
                @click="toggleFavorite(record)"
                class="text-gray-400 hover:text-yellow-500"
                :class="{ 'text-yellow-500': record.is_favorite }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- 加载更多 -->
          <div v-if="hasMore" class="text-center mt-4">
            <button
              @click="loadMore"
              class="text-primary-600 hover:text-primary-500"
              :disabled="loadingMore"
            >
              {{ loadingMore ? '加载中...' : '加载更多' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDivinationHistory, addFavorite, removeFavorite, checkIsFavorite } from '../api/divination'
import { formatDate } from '../utils/common'
import type { DivinationRecord } from '../types'

interface DivinationRecordWithFavorite extends DivinationRecord {
  is_favorite?: boolean
}

const records = ref<DivinationRecordWithFavorite[]>([])
const loading = ref(true)
const loadingMore = ref(false)
const currentPage = ref(0)
const pageSize = 10
const hasMore = ref(true)

const divinationTypes = {
  answer_book: '答案之书',
  tarot: '塔罗牌',
  yijing: '易经',
}

function getDivinationType(type: string) {
  return divinationTypes[type as keyof typeof divinationTypes] || type
}

async function loadRecords(page: number = 0) {
  try {
    const skip = page * pageSize
    const newRecords = await getDivinationHistory({ skip, limit: pageSize })
    const recordsWithFavorite = await Promise.all(
      newRecords.map(async (record) => ({
        ...record,
        is_favorite: await checkIsFavorite(record.id)
      }))
    )
    if (page === 0) {
      records.value = recordsWithFavorite
    } else {
      records.value.push(...recordsWithFavorite)
    }
    hasMore.value = newRecords.length === pageSize
  } catch (error) {
    console.error('获取历史记录失败:', error)
  }
}

async function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  currentPage.value++
  await loadRecords(currentPage.value)
  loadingMore.value = false
}

async function toggleFavorite(record: DivinationRecordWithFavorite) {
  try {
    if (record.is_favorite) {
      await removeFavorite(record.id)
    } else {
      await addFavorite(record.id)
    }
    record.is_favorite = !record.is_favorite
  } catch (error) {
    console.error('收藏操作失败:', error)
  }
}

onMounted(async () => {
  try {
    await loadRecords()
  } finally {
    loading.value = false
  }
})
</script> 