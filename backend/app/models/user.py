"""
用户模型
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    PURCHASER = "purchaser"      # 采购专员
    MANAGER = "manager"          # 部门经理
    ADMIN = "admin"              # 管理员
    SUPER_ADMIN = "super_admin"  # 超级管理员


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.PURCHASER)
    department = Column(String(100))
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    mfa_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tenant = relationship("Tenant", back_populates="users")
    purchase_orders = relationship("PurchaseOrder", back_populates="applicant")