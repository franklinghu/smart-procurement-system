"""
通知 API - 通知管理接口
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.services.notification import notification_manager, NotificationType
from app.core.security import get_current_tenant_id

router = APIRouter()


# ============ Schema ============

class NotificationResponse(BaseModel):
    """通知响应"""
    id: str
    title: str
    content: str
    notification_type: str
    user_id: str
    user_name: str
    read: bool
    created_at: str
    read_at: Optional[str]


class SendNotificationRequest(BaseModel):
    """发送通知请求"""
    user_id: str
    user_name: str
    user_email: str
    notification_type: str
    title: str
    content: str
    channels: Optional[List[str]] = None


class ApprovalNotificationRequest(BaseModel):
    """审批通知请求"""
    approver_id: str
    approver_name: str
    approver_email: str
    order_no: str
    order_title: str
    amount: float
    applicant: str


class ApprovalResultNotificationRequest(BaseModel):
    """审批结果通知请求"""
    applicant_id: str
    applicant_name: str
    applicant_email: str
    order_no: str
    order_title: str
    approved: bool
    reason: Optional[str] = None


# ============ API 接口 ============

@router.get("/messages", response_model=List[NotificationResponse])
async def get_notifications(
    limit: int = Query(20, ge=1, le=100),
    user_id: str = Query(...),
    tenant_id: UUID = Query(None)
):
    """获取通知列表"""
    notifications = await notification_manager.in_site.get_notifications(user_id, limit)
    
    return [
        NotificationResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            notification_type=n.notification_type.value,
            user_id=n.user_id,
            user_name=n.user_name,
            read=n.read,
            created_at=n.created_at.isoformat(),
            read_at=n.read_at.isoformat() if n.read_at else None
        )
        for n in notifications
    ]


@router.get("/messages/unread-count")
async def get_unread_count(
    user_id: str = Query(...),
    tenant_id: UUID = Query(None)
):
    """获取未读数量"""
    count = await notification_manager.in_site.get_unread_count(user_id)
    return {"unread_count": count}


@router.post("/messages/read")
async def mark_notification_read(
    user_id: str = Query(...),
    notification_id: str = Query(...),
    tenant_id: UUID = Query(None)
):
    """标记通知已读"""
    success = await notification_manager.in_site.mark_read(user_id, notification_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {"message": "标记成功"}


@router.post("/messages/read-all")
async def mark_all_notifications_read(
    user_id: str = Query(...),
    tenant_id: UUID = Query(None)
):
    """标记全部已读"""
    success = await notification_manager.in_site.mark_all_read(user_id)
    return {"message": "标记成功"}


@router.post("/send")
async def send_notification(
    request: SendNotificationRequest,
    tenant_id: UUID = Query(None)
):
    """发送通知"""
    channels = request.channels or ["in_site"]
    
    # 转换通知类型
    try:
        notif_type = NotificationType(request.notification_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的通知类型")
    
    results = await notification_manager.send_notification(
        user_id=request.user_id,
        user_name=request.user_name,
        user_email=request.user_email,
        notification_type=notif_type,
        title=request.title,
        content=request.content,
        channels=channels
    )
    
    return {"success": True, "results": results}


@router.post("/approval-notify")
async def send_approval_notification(
    request: ApprovalNotificationRequest,
    tenant_id: UUID = Query(None)
):
    """发送审批通知"""
    results = await notification_manager.send_approval_notification(
        approver_id=request.approver_id,
        approver_name=request.approver_name,
        approver_email=request.approver_email,
        order_no=request.order_no,
        order_title=request.order_title,
        amount=request.amount,
        applicant=request.applicant
    )
    
    return {"success": True, "results": results}


@router.post("/approval-result-notify")
async def send_approval_result_notification(
    request: ApprovalResultNotificationRequest,
    tenant_id: UUID = Query(None)
):
    """发送审批结果通知"""
    results = await notification_manager.send_approval_result_notification(
        applicant_id=request.applicant_id,
        applicant_name=request.applicant_name,
        applicant_email=request.applicant_email,
        order_no=request.order_no,
        order_title=request.order_title,
        approved=request.approved,
        reason=request.reason
    )
    
    return {"success": True, "results": results}