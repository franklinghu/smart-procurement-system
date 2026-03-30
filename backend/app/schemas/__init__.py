"""
Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ===== 用户 Schema =====
class UserBase(BaseModel):
    username: str
    real_name: Optional[str] = None
    role: Optional[str] = "purchaser"
    department: Optional[str] = None


class UserCreate(UserBase):
    password: str
    tenant_id: UUID


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None


class UserResponse(UserBase):
    id: UUID
    tenant_id: UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== 认证 Schema =====
class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


# ===== 租户 Schema =====
class TenantBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    industry: Optional[str] = None
    scale: Optional[str] = None


class TenantCreate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: UUID
    plan: str
    status: str
    language: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== 采购订单 Schema =====
class PurchaseOrderBase(BaseModel):
    goods_name: str
    goods_spec: Optional[str] = None
    quantity: int = Field(gt=0)
    supplier_id: Optional[UUID] = None
    supplier_name: Optional[str] = None
    unit_price: Optional[float] = None
    department: Optional[str] = None
    project_name: Optional[str] = None
    usage: Optional[str] = None
    payment_method: Optional[str] = None
    delivery_place: Optional[str] = None
    delivery_days: Optional[int] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    goods_name: Optional[str] = None
    goods_spec: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    department: Optional[str] = None
    project_name: Optional[str] = None
    usage: Optional[str] = None
    payment_method: Optional[str] = None
    delivery_place: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: UUID
    tenant_id: UUID
    order_no: str
    user_id: UUID
    total_amount: Optional[float]
    status: str
    erp_order_no: Optional[str]
    approval_level: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== 价格 Schema =====
class PriceCompareRequest(BaseModel):
    goods_name: str
    goods_spec: Optional[str] = None
    quantity: int = Field(gt=0)


class PriceResult(BaseModel):
    platform: str
    platform_name: str
    price: Optional[float]
    stock_status: str
    moq: Optional[int]
    delivery_days: Optional[int]
    status: str = "success"  # success, failed, no_stock, no_quote


class PriceCompareResponse(BaseModel):
    task_id: str
    results: list[PriceResult]
    best_match: Optional[dict] = None
    cached: bool = False
    cached_at: Optional[datetime] = None


# ===== 审批 Schema =====
class ApprovalRequest(BaseModel):
    action: str = Field(description: "approve 或 reject")
    comment: Optional[str] = None


class ApprovalRecordResponse(BaseModel):
    id: UUID
    order_id: UUID
    approver_id: UUID
    approver_name: str
    action: str
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True