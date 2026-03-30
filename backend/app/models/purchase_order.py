"""
采购订单模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class OrderStatus(str, enum.Enum):
    DRAFT = "draft"              # 草稿
    PENDING = "pending"          # 待审批
    APPROVED = "approved"         # 已审批
    REJECTED = "rejected"         # 已驳回
    ERP_SYNCED = "erp_synced"     # 已推送ERP
    CLOSED = "closed"             # 已关闭
    WITHDRAWN = "withdrawn"       # 已撤回


class PaymentMethod(str, enum.Enum):
    PRE_PAYMENT = "pre_payment"         # 预付
    MONTHLY_SETTLEMENT = "monthly"       # 月结
    COD = "cod"                           # 货到付款


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    order_no = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # 商品信息
    goods_name = Column(String(255), nullable=False)
    goods_spec = Column(String(500))
    quantity = Column(Integer, nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    supplier_name = Column(String(255))
    unit_price = Column(Numeric(12, 2))
    total_amount = Column(Numeric(12, 2))
    
    # 采购信息
    department = Column(String(100))
    project_name = Column(String(255))
    usage = Column(Text)
    payment_method = Column(Enum(PaymentMethod))
    delivery_place = Column(String(255))
    delivery_days = Column(Integer)
    
    # 状态
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    erp_order_no = Column(String(50))
    
    # 审批
    approval_level = Column(Integer, default=1)  # 1: 一级审批, 2: 二级审批
    
    # 时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tenant = relationship("Tenant", back_populates="purchase_orders")
    applicant = relationship("User", back_populates="purchase_orders")
    supplier = relationship("Supplier")
    approval_records = relationship("ApprovalRecord", back_populates="order")