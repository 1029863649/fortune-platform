from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class UserQuota(Base):
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    type = Column(String(20), nullable=False)  # daily/monthly/yearly
    quota_date = Column(Date, nullable=False)
    quota_count = Column(Integer, default=0)
    
    # 关系
    user = relationship("User", back_populates="quotas")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'type', 'quota_date', name='unique_user_quota'),
    ) 