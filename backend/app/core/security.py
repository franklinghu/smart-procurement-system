"""
安全模块 - 身份验证和授权
"""
from typing import Optional
from uuid import UUID
from fastapi import Header, HTTPException, Depends

# 默认租户ID（开发环境使用）
DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"


async def get_current_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> UUID:
    """
    获取当前租户ID
    开发环境：从 Header x-tenant-id 获取
    生产环境：从 JWT Token 解析
    """
    if x_tenant_id:
        try:
            return UUID(x_tenant_id)
        except ValueError:
            pass
    
    # 开发环境返回默认租户
    return UUID(DEFAULT_TENANT_ID)


async def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> Optional[UUID]:
    """获取当前用户ID"""
    if x_user_id:
        try:
            return UUID(x_user_id)
        except ValueError:
            pass
    return None