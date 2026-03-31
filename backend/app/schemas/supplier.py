"""
供应商 Schema
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal


# ============ 供应商 Schema ============

class SupplierBase(BaseModel):
    """供应商基础字段"""
    name: str = Field(..., description="供应商名称")
    code: Optional[str] = Field(None, description="供应商编码")
    short_name: Optional[str] = Field(None, description="简称")
    contact_name: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[EmailStr] = Field(None, description="联系邮箱")
    address: Optional[str] = Field(None, description="地址")
    business_license: Optional[str] = Field(None, description="营业执照号")
    credit_code: Optional[str] = Field(None, description="统一社会信用代码")
    rating: Optional[Decimal] = Field(5.00, description="评分 0-5")
    credit_level: Optional[str] = Field("A", description="信用等级：A/B/C/D")
    status: Optional[str] = Field("active", description="状态：active/inactive/blocked")
    blocked_reason: Optional[str] = Field(None, description="禁用原因")
    payment_terms: Optional[str] = Field(None, description="付款条款")
    delivery_days: Optional[int] = Field(3, description="默认交货天数")
    min_order_amount: Optional[Decimal] = Field(0, description="最小订单金额")


class SupplierCreate(SupplierBase):
    """创建供应商"""
    pass


class SupplierUpdate(BaseModel):
    """更新供应商"""
    name: Optional[str] = None
    code: Optional[str] = None
    short_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = None
    business_license: Optional[str] = None
    credit_code: Optional[str] = None
    rating: Optional[Decimal] = None
    credit_level: Optional[str] = None
    status: Optional[str] = None
    blocked_reason: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_days: Optional[int] = None
    min_order_amount: Optional[Decimal] = None


class SupplierInDB(SupplierBase):
    """数据库中的供应商"""
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SupplierResponse(SupplierInDB):
    """API 响应"""
    pass


class SupplierListResponse(BaseModel):
    """供应商列表响应"""
    total: int
    items: List[SupplierResponse]


# ============ 供应商平台 Schema ============

class SupplierPlatformBase(BaseModel):
    """供应商平台基础字段"""
    platform: str = Field(..., description="平台：zkh/west/jd/yongyou/kingdee")
    platform_id: Optional[str] = Field(None, description="平台供应商ID")
    platform_name: Optional[str] = Field(None, description="平台店铺名")
    api_key: Optional[str] = Field(None, description="API Key")
    api_secret: Optional[str] = Field(None, description="API Secret")
    api_status: Optional[str] = Field("active", description="连接状态：active/error")


class SupplierPlatformCreate(SupplierPlatformBase):
    """创建供应商平台"""
    pass


class SupplierPlatformUpdate(BaseModel):
    """更新供应商平台"""
    platform: Optional[str] = None
    platform_id: Optional[str] = None
    platform_name: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    api_status: Optional[str] = None


class SupplierPlatformInDB(SupplierPlatformBase):
    """数据库中的供应商平台"""
    id: UUID
    supplier_id: UUID
    last_sync_at: Optional[datetime]
    sync_error: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SupplierPlatformResponse(SupplierPlatformInDB):
    """API 响应"""
    pass


class SupplierWithPlatformsResponse(SupplierResponse):
    """带平台的供应商"""
    platforms: List[SupplierPlatformResponse] = []