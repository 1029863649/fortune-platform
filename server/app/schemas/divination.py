from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class DivinationBase(BaseModel):
    type: str  # answer_book/tarot/yijing
    question: str

class DivinationCreate(DivinationBase):
    pass

class DivinationUpdate(DivinationBase):
    answer: Optional[str] = None

class DivinationInDBBase(DivinationBase):
    id: UUID4
    user_id: UUID4
    answer: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Divination(DivinationInDBBase):
    pass

class DivinationInDB(DivinationInDBBase):
    pass 