<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">我的收藏</h3>
        
        <!-- 收藏列表 -->
        <div class="mt-6 space-y-6">
          <div v-if="loading" class="text-center py-4">
            <div class="text-gray-500">加载中...</div>
          </div>
          
          <div v-else-if="favorites.length === 0" class="text-center py-4">
            <div class="text-gray-500">暂无收藏记录</div>
          </div>
          
          <div v-else v-for="favorite in favorites" :key="favorite.id" class="bg-gray-50 p-4 rounded-lg">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-sm text-gray-500">
                  {{ formatDate(favorite.created_at) }}
                  <span class="mx-2">·</span>
                  {{ getDivinationType(favorite.record?.type) }}
                </div>
                <div class="mt-2 text-gray-900 font-medium">{{ favorite.record?.question }}</div>
                <div class="mt-2 text-gray-600 whitespace-pre-line">{{ favorite.record?.answer }}</div>
              </div>
              <button
                @click="removeFavorite(favorite)"
                class="text-yellow-500 hover:text-gray-400"
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
import { getFavorites, removeFavorite as removeFavoriteApi } from '../api/favorite'
import { formatDate } from '../utils/common'
import type { Favorite } from '../types'

const favorites = ref<Favorite[]>([])
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

function getDivinationType(type: string | undefined) {
  if (!type) return ''
  return divinationTypes[type as keyof typeof divinationTypes] || type
}

async function loadFavorites(page: number = 0) {
  try {
    const skip = page * pageSize
    const response = await getFavorites({ skip, limit: pageSize })
    if (page === 0) {
      favorites.value = response.items
    } else {
      favorites.value.push(...response.items)
    }
    hasMore.value = response.items.length === pageSize
  } catch (error) {
    console.error('获取收藏记录失败:', error)
  }
}

async function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  currentPage.value++
  await loadFavorites(currentPage.value)
  loadingMore.value = false
}

async function removeFavorite(favorite: Favorite) {
  try {
    await removeFavoriteApi(favorite.record_id)
    favorites.value = favorites.value.filter(f => f.id !== favorite.id)
  } catch (error) {
    console.error('取消收藏失败:', error)
  }
}

onMounted(async () => {
  try {
    await loadFavorites()
  } finally {
    loading.value = false
  }
})
</script> 