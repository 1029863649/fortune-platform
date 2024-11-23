from sqlalchemy import Column, Date, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid

class CheckIn(Base):
    """签到记录模型"""
    __tablename__ = "checkins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    check_date = Column(Date, nullable=False)
    reward = Column(Integer, nullable=False, comment="获得的奖励配额")

    # 关系
    user = relationship("User", back_populates="checkins")

    # 约束和索引
    __table_args__ = (
        UniqueConstraint('user_id', 'check_date', name='uq_user_check_date'),
        Index('ix_checkins_user_date', 'user_id', 'check_date'),
    )

    def __repr__(self):
        return f"<CheckIn(user_id={self.user_id}, date={self.check_date}, reward={self.reward})>"

    @property
    def is_today(self) -> bool:
        """判断是否为今日签到"""
        from datetime import date
        return self.check_date == date.today()

    class Config:
        orm_mode = True 