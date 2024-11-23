export interface CheckInResponse {
  success: boolean
  message: string
  streak: number
  reward: number
}

export interface CheckInStatus {
  checked: boolean
  streak: number
  next_reward: number
}

export interface CheckInHistory {
  date: string
  checked: boolean
  reward?: number
}

export interface CheckInStats {
  total_days: number
  total_rewards: number
  max_streak: number
  current_streak: number
  history: CheckInHistory[]
}

export interface CheckInApiResponse {
  status: 'success' | 'error'
  data?: {
    streak: number
    reward: number
  }
  message?: string
}

export interface CheckInState {
  streak: number
  checked: boolean
  loading: boolean
  last7Days: CheckInHistory[]
  stats: CheckInStats | null
  nextReward: number
} 