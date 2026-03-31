"""
ERP API - ERP对接接口
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.services.erp.yongyou_u8 import (
    erp_manager, 
    YongyouU8Adapter, 
    SyncStatus,
    PurchaseOrder,
    ERPSyncRecord
)
from app.core.security import get_current_tenant_id

router = APIRouter()


# ============ Schema ============

class ERPConfigRequest(BaseModel):
    """ERP配置"""
    erp_type: str = "yongyou_u8"
    host: str
    app_id: str
    app_key: str
    user: str
    password: str


class ERPConfigResponse(BaseModel):
    """ERP配置响应"""
    erp_type: str
    erp_name: str
    host: str
    user: str
    is_active: bool


class SyncRequest(BaseModel):
    """同步请求"""
    order_id: str
    order_no: str
    supplier_id: str
    supplier_name: str
    total_amount: float
    payment_method: str
    delivery_place: str
    items: List[dict]


class SyncResponse(BaseModel):
    """同步响应"""
    sync_id: str
    order_id: str
    order_no: str
    erp_order_id: Optional[str]
    erp_order_no: Optional[str]
    status: str
    error_message: Optional[str]
    retry_count: int
    created_at: str
    synced_at: Optional[str]


class TestConnectionResponse(BaseModel):
    """测试连接响应"""
    success: bool
    message: str
    erp_name: str


# ============ API 接口 ============

@router.get("/configs", response_model=List[ERPConfigResponse])
async def get_erp_configs(
    tenant_id: UUID = Query(None)
):
    """获取ERP配置列表"""
    return [
        ERPConfigResponse(
            erp_type="yongyou_u8",
            erp_name="用友U8",
            host="http://u8-server:8088",
            user="admin",
            is_active=True
        )
    ]


@router.post("/configs", response_model=ERPConfigResponse)
async def create_erp_config(
    config: ERPConfigRequest,
    tenant_id: UUID = Query(None)
):
    """创建ERP配置"""
    if config.erp_type == "yongyou_u8":
        adapter = YongyouU8Adapter(
            host=config.host,
            app_id=config.app_id,
            app_key=config.app_key,
            user=config.user,
            password=config.password
        )
        erp_manager.register_adapter(adapter)
    
    return ERPConfigResponse(
        erp_type=config.erp_type,
        erp_name="用友U8",
        host=config.host,
        user=config.user,
        is_active=True
    )


@router.post("/configs/test", response_model=TestConnectionResponse)
async def test_erp_connection(
    config: ERPConfigRequest,
    tenant_id: UUID = Query(None)
):
    """测试ERP连接"""
    try:
        if config.erp_type == "yongyou_u8":
            adapter = YongyouU8Adapter(
                host=config.host,
                app_id=config.app_id,
                app_key=config.app_key,
                user=config.user,
                password=config.password
            )
            success = await adapter.test_connection()
            
            return TestConnectionResponse(
                success=success,
                message="连接成功" if success else "连接失败",
                erp_name="用友U8"
            )
    except Exception as e:
        return TestConnectionResponse(
            success=False,
            message=f"连接异常: {str(e)}",
            erp_name=config.erp_type
        )


@router.post("/sync/orders", response_model=SyncResponse)
async def sync_order_to_erp(
    request: SyncRequest,
    erp_type: str = Query("yongyou_u8"),
    tenant_id: UUID = Query(None)
):
    """同步采购订单到ERP"""
    # 创建订单对象
    order = PurchaseOrder(
        order_id=request.order_id,
        order_no=request.order_no,
        tenant_id=str(tenant_id) if tenant_id else "default",
        supplier_id=request.supplier_id,
        supplier_name=request.supplier_name,
        total_amount=request.total_amount,
        payment_method=request.payment_method,
        delivery_place=request.delivery_place,
        items=request.items,
        status="pending",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # 执行同步
    record = await erp_manager.sync_order(order, erp_type)
    
    return SyncResponse(
        sync_id=record.id,
        order_id=record.order_id,
        order_no=record.order_no,
        erp_order_id=record.erp_order_id,
        erp_order_no=record.erp_order_no,
        status=record.status.value,
        error_message=record.error_message,
        retry_count=record.retry_count,
        created_at=record.created_at.isoformat(),
        synced_at=record.synced_at.isoformat() if record.synced_at else None
    )


@router.get("/sync/orders", response_model=List[SyncResponse])
async def get_sync_records(
    order_id: str = Query(None),
    tenant_id: UUID = Query(None)
):
    """获取同步记录列表"""
    records = erp_manager.get_sync_records(order_id)
    
    return [
        SyncResponse(
            sync_id=r.id,
            order_id=r.order_id,
            order_no=r.order_no,
            erp_order_id=r.erp_order_id,
            erp_order_no=r.erp_order_no,
            status=r.status.value,
            error_message=r.error_message,
            retry_count=r.retry_count,
            created_at=r.created_at.isoformat(),
            synced_at=r.synced_at.isoformat() if r.synced_at else None
        )
        for r in records
    ]


@router.post("/sync/orders/{sync_id}/retry", response_model=SyncResponse)
async def retry_sync(
    sync_id: str,
    tenant_id: UUID = Query(None)
):
    """重试同步"""
    record = await erp_manager.retry_sync(sync_id)
    
    return SyncResponse(
        sync_id=record.id,
        order_id=record.order_id,
        order_no=record.order_no,
        erp_order_id=record.erp_order_id,
        erp_order_no=record.erp_order_no,
        status=record.status.value,
        error_message=record.error_message,
        retry_count=record.retry_count,
        created_at=record.created_at.isoformat(),
        synced_at=record.synced_at.isoformat() if record.synced_at else None
    )