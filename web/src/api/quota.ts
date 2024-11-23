import http from '../utils/http'
import type { Quota } from '../types'

export async function getQuota(): Promise<Quota> {
  const response = await http.get<Quota>('/quota/me')
  return response
}

export async function checkQuota(): Promise<boolean> {
  try {
    const quota = await getQuota()
    return quota.remaining > 0
  } catch {
    return false
  }
}

export async function getQuotaReset(): Promise<string> {
  const quota = await getQuota()
  return quota.reset_time
}

export async function getVipQuota(): Promise<{
  daily_limit: number
  vip_level: number
  vip_expire?: string
}> {
  const response = await http.get('/quota/vip')
  return response
} 