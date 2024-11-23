from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class DivinationRecord(Base):
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    type = Column(String(20), nullable=False)  # answer_book/tarot/yijing
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # 关系
    user = relationship("User", back_populates="divination_records") 