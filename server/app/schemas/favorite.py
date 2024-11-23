from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime
from .divination import Divination

class FavoriteBase(BaseModel):
    record_id: UUID4

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteInDBBase(FavoriteBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Favorite(FavoriteInDBBase):
    record: Optional[Divination] = None

class FavoriteInDB(FavoriteInDBBase):
    pass 