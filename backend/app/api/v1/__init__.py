"""
API 路由入口
"""
from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    goods,
    prices,
    purchases,
    approvals,
    erp,
    tenants,
    suppliers,
    notifications
)

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(goods.router, prefix="/goods", tags=["商品"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["供应商"])
api_router.include_router(prices.router, prefix="/prices", tags=["价格"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["采购"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["审批"])
api_router.include_router(erp.router, prefix="/erp", tags=["ERP"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["通知"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["租户"])