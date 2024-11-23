from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class QuotaBase(BaseModel):
    type: str  # daily/monthly/yearly
    quota_date: date
    quota_count: int = 0

class QuotaCreate(QuotaBase):
    user_id: UUID4

class QuotaUpdate(QuotaBase):
    pass

class QuotaInDBBase(QuotaBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Quota(QuotaInDBBase):
    pass 