from datetime import date
from typing import Optional, List
from pydantic import BaseModel, UUID4, Field

class CheckInBase(BaseModel):
    """签到基础模型"""
    user_id: UUID4
    check_date: date
    reward: int = Field(..., description="获得的奖励配额")

class CheckInCreate(CheckInBase):
    """创建签到记录"""
    pass

class CheckInInDB(CheckInBase):
    """数据库中的签到记录"""
    id: UUID4
    
    class Config:
        from_attributes = True

class CheckInResponse(BaseModel):
    """签到响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="提示信息")
    streak: int = Field(..., description="连续签到天数")
    reward: int = Field(..., description="获得的奖励")

class CheckInStatus(BaseModel):
    """签到状态"""
    checked: bool = Field(..., description="今日是否已签到")
    streak: int = Field(..., description="连续签到天数")
    next_reward: int = Field(..., description="下次签到奖励")

class CheckInHistory(BaseModel):
    """签到历史记录"""
    date: date = Field(..., description="签到日期")
    checked: bool = Field(..., description="是否已签到")
    reward: Optional[int] = Field(None, description="获得的奖励")

class CheckInStats(BaseModel):
    """签到统计"""
    total_days: int = Field(..., description="总签到天数")
    total_rewards: int = Field(..., description="总获得奖励")
    max_streak: int = Field(..., description="最大连续签到天数")
    current_streak: int = Field(..., description="当前连续签到天数")
    history: List[CheckInHistory] = Field(default_factory=list, description="签到历史")