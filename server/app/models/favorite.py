from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Favorite(Base):
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    record_id = Column(UUID(as_uuid=True), ForeignKey("divinationrecord.id"), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="favorites")
    record = relationship("DivinationRecord", back_populates="favorites")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'record_id', name='unique_favorite'),
    ) 