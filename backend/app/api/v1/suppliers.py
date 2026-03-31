"""
供应商 API
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_tenant_id
from app.models.supplier import Supplier, SupplierPlatform
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
    SupplierListResponse,
    SupplierWithPlatformsResponse,
    SupplierPlatformCreate,
    SupplierPlatformUpdate,
    SupplierPlatformResponse,
)

router = APIRouter()


# ============ 供应商接口 ============

@router.get("", response_model=SupplierListResponse)
def get_suppliers(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    status: Optional[str] = Query(None, description="状态过滤"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """获取供应商列表"""
    query = db.query(Supplier).filter(Supplier.tenant_id == tenant_id)
    
    if status:
        query = query.filter(Supplier.status == status)
    
    if keyword:
        query = query.filter(
            (Supplier.name.ilike(f"%{keyword}%")) | 
            (Supplier.code.ilike(f"%{keyword}%")) |
            (Supplier.short_name.ilike(f"%{keyword}%"))
        )
    
    total = query.count()
    items = query.order_by(Supplier.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


@router.get("/{supplier_id}", response_model=SupplierWithPlatformsResponse)
def get_supplier(
    supplier_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """获取供应商详情（包含平台列表）"""
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    return supplier


@router.post("", response_model=SupplierResponse, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """创建供应商"""
    # 检查编码是否重复
    if supplier.code:
        existing = db.query(Supplier).filter(
            Supplier.tenant_id == tenant_id,
            Supplier.code == supplier.code
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="供应商编码已存在")
    
    db_supplier = Supplier(
        **supplier.model_dump(),
        tenant_id=tenant_id
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: UUID,
    supplier: SupplierUpdate,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """更新供应商"""
    db_supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    # 检查编码是否重复
    if supplier.code and supplier.code != db_supplier.code:
        existing = db.query(Supplier).filter(
            Supplier.tenant_id == tenant_id,
            Supplier.code == supplier.code,
            Supplier.id != supplier_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="供应商编码已存在")
    
    update_data = supplier.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_supplier, field, value)
    
    db.commit()
    db.refresh(db_supplier)
    
    return db_supplier


@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """删除供应商"""
    db_supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    db.delete(db_supplier)
    db.commit()
    
    return {"message": "删除成功"}


@router.patch("/{supplier_id}/status")
def update_supplier_status(
    supplier_id: UUID,
    status: str = Query(..., description="状态：active/inactive/blocked"),
    blocked_reason: Optional[str] = Query(None, description="禁用原因"),
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """更新供应商状态"""
    db_supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    db_supplier.status = status
    if status == "blocked":
        db_supplier.blocked_reason = blocked_reason
    
    db.commit()
    
    return {"message": "状态更新成功", "status": status}


# ============ 供应商平台接口 ============

@router.get("/{supplier_id}/platforms", response_model=List[SupplierPlatformResponse])
def get_supplier_platforms(
    supplier_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """获取供应商的平台列表"""
    # 验证供应商属于当前租户
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    platforms = db.query(SupplierPlatform).filter(
        SupplierPlatform.supplier_id == supplier_id
    ).all()
    
    return platforms


@router.post("/{supplier_id}/platforms", response_model=SupplierPlatformResponse, status_code=201)
def create_supplier_platform(
    supplier_id: UUID,
    platform: SupplierPlatformCreate,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """创建供应商平台"""
    # 验证供应商属于当前租户
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    # 检查平台是否重复
    existing = db.query(SupplierPlatform).filter(
        SupplierPlatform.supplier_id == supplier_id,
        SupplierPlatform.platform == platform.platform
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="该平台已添加")
    
    db_platform = SupplierPlatform(
        **platform.model_dump(),
        supplier_id=supplier_id
    )
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    
    return db_platform


@router.delete("/{supplier_id}/platforms/{platform_id}")
def delete_supplier_platform(
    supplier_id: UUID,
    platform_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """删除供应商平台"""
    # 验证供应商属于当前租户
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.tenant_id == tenant_id
    ).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    db_platform = db.query(SupplierPlatform).filter(
        SupplierPlatform.id == platform_id,
        SupplierPlatform.supplier_id == supplier_id
    ).first()
    
    if not db_platform:
        raise HTTPException(status_code=404, detail="平台不存在")
    
    db.delete(db_platform)
    db.commit()
    
    return {"message": "删除成功"}