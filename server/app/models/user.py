from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    vip_level = Column(Integer, default=0)
    vip_expire = Column(DateTime, nullable=True)
    settings = Column(JSON, default={
        "email_notification": True,
        "browser_notification": False,
        "public_history": False,
        "public_favorites": False,
        "theme": "light",
        "check_in_reminder": True,
        "public_check_in": False
    })
    divination_records = relationship("DivinationRecord", back_populates="user", cascade="all, delete-orphan")
    quotas = relationship("UserQuota", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    checkins = relationship("CheckIn", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"