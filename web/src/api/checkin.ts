import http from '../utils/http'
import type { 
    CheckInResponse, 
    CheckInStatus, 
    CheckInHistory, 
    CheckInStats 
} from '../types/checkin'

/**
 * 执行签到
 */
export async function checkIn(): Promise<CheckInResponse> {
    const response = await http.post<CheckInResponse>('/checkin')
    return response
}

/**
 * 获取签到状态
 */
export async function getCheckInStatus(): Promise<CheckInStatus> {
    const response = await http.get<CheckInStatus>('/checkin/status')
    return response
}

/**
 * 获取签到历史
 * @param days 获取天数，默认7天
 */
export async function getCheckInHistory(days: number = 7): Promise<CheckInHistory[]> {
    const response = await http.get<CheckInHistory[]>('/checkin/history', {
        params: { days }
    })
    return response
}

/**
 * 获取签到统计
 */
export async function getCheckInStats(): Promise<CheckInStats> {
    const response = await http.get<CheckInStats>('/checkin/stats')
    return response
}

/**
 * 获取连续签到天数和下次奖励
 */
export async function getStreak(): Promise<{
    streak: number
    next_reward: number
}> {
    const response = await http.get('/checkin/streak')
    return response
} 