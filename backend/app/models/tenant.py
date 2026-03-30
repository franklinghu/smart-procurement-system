"""
租户模型
"""
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class TenantPlan(str, enum.Enum):
    BASIC = "basic"      # 基础版
    PRO = "pro"          # 专业版
    ENTERPRISE = "enterprise"  # 企业版


class TenantStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    TRIAL = "trial"


class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    short_name = Column(String(100))
    logo = Column(String(500))
    industry = Column(String(50))
    scale = Column(String(20))
    plan = Column(Enum(TenantPlan), default=TenantPlan.BASIC)
    status = Column(Enum(TenantStatus), default=TenantStatus.TRIAL)
    language = Column(String(10), default="zh-CN")
    timezone = Column(String(50), default="Asia/Shanghai")
    theme_primary = Column(String(20), default="#409EFF")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    users = relationship("User", back_populates="tenant")
    purchase_orders = relationship("PurchaseOrder", back_populates="tenant")