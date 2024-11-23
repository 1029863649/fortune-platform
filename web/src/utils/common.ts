// 日期格式化
export function formatDate(dateStr: string, format: string = 'YYYY-MM-DD HH:mm:ss'): string {
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

// 占卜类型映射
export const divinationTypes = {
  answer_book: '答案之书',
  tarot: '塔罗牌',
  yijing: '易经',
} as const

export type DivinationType = keyof typeof divinationTypes

// 获取占卜类型显示名称
export function getDivinationTypeName(type: DivinationType): string {
  return divinationTypes[type]
}

// VIP等级映射
export const vipLevels = {
  0: '普通用户',
  1: 'VIP用户',
  2: '高级VIP用户',
} as const

export type VipLevel = keyof typeof vipLevels

// 获取VIP等级显示名称
export function getVipLevelName(level: VipLevel): string {
  return vipLevels[level]
}

// 错误消息处理
export function getErrorMessage(error: any): string {
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }
  return error.message || '发生未知错误'
} 