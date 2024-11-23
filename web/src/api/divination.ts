import http from '../utils/http'
import type { DivinationRecord, PaginatedResponse } from '../types'

interface DivinationRequest {
  type: 'answer_book' | 'tarot' | 'yijing'
  question: string
}

export async function createDivination(data: DivinationRequest): Promise<DivinationRecord> {
  const response = await http.post<DivinationRecord>('/divination', data)
  return response
}

export async function getDivinationHistory(params: { skip?: number; limit?: number } = {}): Promise<DivinationRecord[]> {
  const response = await http.get<PaginatedResponse<DivinationRecord>>('/divination/me', { params })
  return response.items
}

export async function getDivination(id: string): Promise<DivinationRecord> {
  const response = await http.get<DivinationRecord>(`/divination/${id}`)
  return response
}

export async function addFavorite(recordId: string): Promise<void> {
  await http.post('/favorites', { record_id: recordId })
}

export async function removeFavorite(recordId: string): Promise<void> {
  await http.delete(`/favorites/${recordId}`)
}

export async function checkIsFavorite(recordId: string): Promise<boolean> {
  try {
    await http.get(`/favorites/${recordId}`)
    return true
  } catch {
    return false
  }
} 