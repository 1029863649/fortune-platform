<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">在线占卜</h3>
        
        <!-- 配额信息 -->
        <div class="mt-2 text-sm text-gray-500">
          今日剩余次数: {{ quota.remaining }}/{{ quota.daily_limit }}
          <span class="ml-2">重置时间: {{ formatDate(quota.reset_time) }}</span>
        </div>

        <!-- 占卜类型选择 -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-700">选择占卜类型</label>
          <div class="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <button
              v-for="(name, type) in divinationTypes"
              :key="type"
              @click="selectedType = type"
              class="relative px-4 py-3 border rounded-lg shadow-sm"
              :class="[
                selectedType === type
                  ? 'border-primary-500 ring-2 ring-primary-500'
                  : 'border-gray-300 hover:border-gray-400'
              ]"
            >
              <span class="block text-sm font-medium text-gray-900">{{ name }}</span>
            </button>
          </div>
        </div>

        <!-- 问题输入 -->
        <div class="mt-6">
          <label for="question" class="block text-sm font-medium text-gray-700">
            输入您的问题
          </label>
          <div class="mt-2">
            <textarea
              id="question"
              v-model="question"
              rows="3"
              class="shadow-sm block w-full focus:ring-primary-500 focus:border-primary-500 sm:text-sm border border-gray-300 rounded-md"
              :placeholder="getPlaceholder()"
              :disabled="loading"
            ></textarea>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="mt-6">
          <button
            @click="submitDivination"
            class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="!canSubmit || loading"
          >
            {{ loading ? '正在占卜...' : '开始占卜' }}
          </button>
        </div>

        <!-- 占卜结果 -->
        <div v-if="result" class="mt-6">
          <div class="rounded-md bg-gray-50 p-4">
            <div class="text-sm text-gray-700 whitespace-pre-line">
              {{ result.answer }}
            </div>
            <div class="mt-4 flex justify-end">
              <button
                @click="toggleFavorite"
                class="text-gray-400 hover:text-yellow-500"
                :class="{ 'text-yellow-500': isFavorite }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { createDivination, addFavorite, removeFavorite } from '../api/divination'
import { getQuota } from '../api/quota'
import { formatDate } from '../utils/common'
import type { DivinationRecord, Quota } from '../types'

const divinationTypes = {
  answer_book: '答案之书',
  tarot: '塔罗牌',
  yijing: '易经',
} as const

const selectedType = ref<keyof typeof divinationTypes>('answer_book')
const question = ref('')
const loading = ref(false)
const result = ref<DivinationRecord | null>(null)
const isFavorite = ref(false)
const quota = ref<Quota>({
  daily_limit: 0,
  used_today: 0,
  remaining: 0,
  reset_time: new Date().toISOString()
})

const canSubmit = computed(() => {
  return selectedType.value && 
         question.value.trim().length > 0 && 
         quota.value.remaining > 0
})

function getPlaceholder() {
  switch (selectedType.value) {
    case 'answer_book':
      return '请输入一个是/否问题...'
    case 'tarot':
      return '请描述您想要解答的问题...'
    case 'yijing':
      return '请描述您的困惑...'
    default:
      return '请输入您的问题...'
  }
}

async function submitDivination() {
  if (!canSubmit.value || loading.value) return
  
  loading.value = true
  try {
    result.value = await createDivination({
      type: selectedType.value,
      question: question.value.trim()
    })
    isFavorite.value = false
    await updateQuota()
  } catch (error) {
    console.error('占卜失败:', error)
  } finally {
    loading.value = false
  }
}

async function toggleFavorite() {
  if (!result.value) return
  
  try {
    if (isFavorite.value) {
      await removeFavorite(result.value.id)
    } else {
      await addFavorite(result.value.id)
    }
    isFavorite.value = !isFavorite.value
  } catch (error) {
    console.error('收藏操作失败:', error)
  }
}

async function updateQuota() {
  try {
    quota.value = await getQuota()
  } catch (error) {
    console.error('获取配额信息失败:', error)
  }
}

onMounted(async () => {
  await updateQuota()
})
</script> 