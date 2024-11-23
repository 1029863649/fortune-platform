import http from '../utils/http'
import type { Stats, TrendData } from '../types'

export async function getUserStats(): Promise<Stats> {
  const response = await http.get<Stats>('/stats/me')
  return response
}

export async function getTrendData(days: number = 7): Promise<TrendData> {
  const response = await http.get<TrendData>('/stats/trends', {
    params: { days }
  })
  return response
}

export async function getTypeStats(): Promise<Record<string, number>> {
  const response = await http.get<Record<string, number>>('/stats/types')
  return response
}

export async function getFavoriteStats(): Promise<Record<string, number>> {
  const response = await http.get<Record<string, number>>('/stats/favorites')
  return response
} 