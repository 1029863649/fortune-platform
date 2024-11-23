import http from '../utils/http'
import type { Favorite, PaginatedResponse } from '../types'

export async function getFavorites(params: { skip?: number; limit?: number } = {}): Promise<PaginatedResponse<Favorite>> {
  const response = await http.get<PaginatedResponse<Favorite>>('/favorites/me', { params })
  return response
}

export async function addFavorite(recordId: string): Promise<Favorite> {
  const response = await http.post<Favorite>('/favorites', { record_id: recordId })
  return response
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