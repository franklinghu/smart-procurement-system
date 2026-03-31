"""
供应商模型
"""
from sqlalchemy import Column, String, DateTime, Numeric, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: __import__('uuid').uuid4())
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    # 基本信息
    name = Column(String(255), nullable=False, comment="供应商名称")
    code = Column(String(50), comment="供应商编码")
    short_name = Column(String(100), comment="简称")
    
    # 联系方式
    contact_name = Column(String(100), comment="联系人")
    contact_phone = Column(String(20), comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")
    address = Column(String(500), comment="地址")
    
    # 企业信息
    business_license = Column(String(100), comment="营业执照号")
    credit_code = Column(String(100), comment="统一社会信用代码")
    
    # 评级
    rating = Column(Numeric(3, 2), default=5.00, comment="评分 0-5")
    credit_level = Column(String(20), default="A", comment="信用等级：A/B/C/D")
    
    # 状态
    status = Column(String(20), default="active", comment="状态：active/inactive/blocked")
    blocked_reason = Column(String(500), comment="禁用原因")
    
    # 扩展
    payment_terms = Column(String(50), comment="付款条款")
    delivery_days = Column(Integer, default=3, comment="默认交货天数")
    min_order_amount = Column(Numeric(12, 2), default=0, comment="最小订单金额")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tenant = relationship("Tenant", back_populates="suppliers")
    platforms = relationship("SupplierPlatform", back_populates="supplier", cascade="all, delete-orphan")


class SupplierPlatform(Base):
    __tablename__ = "supplier_platforms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: __import__('uuid').uuid4())
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False, comment="平台：zkh/west/jd/yongyou/kingdee")
    platform_id = Column(String(100), comment="平台供应商ID")
    platform_name = Column(String(255), comment="平台店铺名")
    
    # API配置
    api_key = Column(String(500), comment="API Key")
    api_secret = Column(String(500), comment="API Secret")
    api_status = Column(String(20), default="active", comment="连接状态：active/error")
    last_sync_at = Column(DateTime, comment="最后同步时间")
    sync_error = Column(Text, comment="同步错误信息")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    supplier = relationship("Supplier", back_populates="platforms")