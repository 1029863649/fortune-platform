import http from '../utils/http'
import type { Settings } from '../types'

export async function getSettings(): Promise<Settings> {
  const response = await http.get<Settings>('/users/me/settings')
  return response
}

export async function updateSettings(settings: Partial<Settings>): Promise<Settings> {
  const response = await http.put<Settings>('/users/me/settings', settings)
  return response
} 