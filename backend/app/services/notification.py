"""
通知服务 - 站内信 + 邮件通知
"""
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import asyncio


class NotificationType(str, Enum):
    """通知类型"""
    APPROVAL_REQUIRED = "approval_required"  # 待审批
    APPROVED = "approved"                    # 已通过
    REJECTED = "rejected"                    # 已驳回
    ORDER_SUBMITTED = "order_submitted"      # 订单已提交
    ORDER_SYNCED = "order_synced"            # 已同步到ERP
    ORDER_TIMEOUT = "order_timeout"          # 审批超时
    SYSTEM = "system"                         # 系统通知


class NotificationChannel(str, Enum):
    """通知渠道"""
    IN_SITE = "in_site"   # 站内信
    EMAIL = "email"       # 邮件
    SMS = "sms"           # 短信


@dataclass
class Notification:
    """通知"""
    id: str
    title: str
    content: str
    notification_type: NotificationType
    user_id: str
    user_name: str
    read: bool = False
    channels: List[NotificationChannel] = None
    created_at: datetime = None
    read_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.channels is None:
            self.channels = [NotificationChannel.IN_SITE]
        if self.created_at is None:
            self.created_at = datetime.now()


class InSiteNotifier:
    """站内信通知"""
    
    def __init__(self):
        self.notifications: Dict[str, List[Notification]] = {}
    
    async def send(self, notification: Notification) -> bool:
        """发送站内信"""
        user_id = notification.user_id
        
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        
        self.notifications[user_id].append(notification)
        return True
    
    async def get_unread_count(self, user_id: str) -> int:
        """获取未读数量"""
        if user_id not in self.notifications:
            return 0
        
        return sum(1 for n in self.notifications[user_id] if not n.read)
    
    async def get_notifications(self, user_id: str, limit: int = 20) -> List[Notification]:
        """获取通知列表"""
        if user_id not in self.notifications:
            return []
        
        return sorted(
            self.notifications[user_id], 
            key=lambda x: x.created_at, 
            reverse=True
        )[:limit]
    
    async def mark_read(self, user_id: str, notification_id: str) -> bool:
        """标记已读"""
        if user_id not in self.notifications:
            return False
        
        for n in self.notifications[user_id]:
            if n.id == notification_id:
                n.read = True
                n.read_at = datetime.now()
                return True
        
        return False
    
    async def mark_all_read(self, user_id: str) -> bool:
        """标记全部已读"""
        if user_id not in self.notifications:
            return False
        
        for n in self.notifications[user_id]:
            n.read = True
            n.read_at = datetime.now()
        
        return True


class EmailNotifier:
    """邮件通知"""
    
    def __init__(self, smtp_host: str = "", smtp_port: int = 587,
                 username: str = "", password: str = ""):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    async def send(self, to: str, subject: str, content: str, 
                   html: bool = False) -> bool:
        """
        发送邮件
        实际项目中调用SMTP或邮件服务API
        """
        # 模拟发送
        print(f"[Email] To: {to}, Subject: {subject}")
        
        # 实际项目中：
        # import aiosmtplib
        # message = MIMEText(content, 'html' if html else 'plain')
        # message['Subject'] = subject
        # message['From'] = self.username
        # message['To'] = to
        # await aiosmtplib.send(message, hostname=self.smtp_host, port=self.smtp_port)
        
        return True
    
    async def send_template(self, to: str, template: str, **kwargs) -> bool:
        """发送模板邮件"""
        templates = {
            "approval_required": {
                "subject": "【智能采购系统】待审批提醒",
                "content": "您有一个采购申请需要审批，点击查看详情"
            },
            "approved": {
                "subject": "【智能采购系统】审批通过",
                "content": "您的采购申请已通过审批"
            },
            "rejected": {
                "subject": "【智能采购系统】审批驳回",
                "content": "您的采购申请已被驳回，原因：{reason}"
            },
            "order_synced": {
                "subject": "【智能采购系统】订单已同步ERP",
                "content": "采购订单已成功同步到ERP系统"
            }
        }
        
        template_data = templates.get(template, {})
        content = template_data.get("content", "").format(**kwargs)
        
        return await self.send(to, template_data.get("subject", ""), content)


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.in_site = InSiteNotifier()
        self.email = EmailNotifier()
    
    async def send_notification(
        self,
        user_id: str,
        user_name: str,
        user_email: str,
        notification_type: NotificationType,
        title: str,
        content: str,
        channels: List[NotificationChannel] = None
    ) -> Dict[str, bool]:
        """发送通知"""
        import uuid
        
        if channels is None:
            channels = [NotificationChannel.IN_SITE]
        
        results = {}
        
        # 站内信
        if NotificationChannel.IN_SITE in channels:
            notification = Notification(
                id=str(uuid.uuid4()),
                title=title,
                content=content,
                notification_type=notification_type,
                user_id=user_id,
                user_name=user_name
            )
            results['in_site'] = await self.in_site.send(notification)
        
        # 邮件
        if NotificationChannel.EMAIL in channels and user_email:
            email_template = {
                NotificationType.APPROVAL_REQUIRED: "approval_required",
                NotificationType.APPROVED: "approved",
                NotificationType.REJECTED: "rejected",
                NotificationType.ORDER_SYNCED: "order_synced"
            }
            
            template_key = email_template.get(notification_type)
            if template_key:
                results['email'] = await self.email.send_template(
                    user_email, 
                    template_key,
                    reason=content  # 用于驳回原因
                )
            else:
                results['email'] = await self.email.send(
                    user_email, title, content
                )
        
        return results
    
    async def send_approval_notification(
        self,
        approver_id: str,
        approver_name: str,
        approver_email: str,
        order_no: str,
        order_title: str,
        amount: float,
        applicant: str
    ):
        """发送审批通知"""
        title = f"审批提醒：{order_title}"
        content = f"采购单号：{order_no}\n金额：¥{amount:,.2f}\n申请人：{applicant}"
        
        return await self.send_notification(
            user_id=approver_id,
            user_name=approver_name,
            user_email=approver_email,
            notification_type=NotificationType.APPROVAL_REQUIRED,
            title=title,
            content=content,
            channels=[NotificationChannel.IN_SITE, NotificationChannel.EMAIL]
        )
    
    async def send_approval_result_notification(
        self,
        applicant_id: str,
        applicant_name: str,
        applicant_email: str,
        order_no: str,
        order_title: str,
        approved: bool,
        reason: str = None
    ):
        """发送审批结果通知"""
        notification_type = NotificationType.APPROVED if approved else NotificationType.REJECTED
        title = f"审批结果：{'通过' if approved else '驳回'} - {order_title}"
        content = f"采购单号：{order_no}\n"
        if approved:
            content += "您的采购申请已通过审批"
        else:
            content += f"您的采购申请已被驳回\n驳回原因：{reason}"
        
        return await self.send_notification(
            user_id=applicant_id,
            user_name=applicant_name,
            user_email=applicant_email,
            notification_type=notification_type,
            title=title,
            content=content,
            channels=[NotificationChannel.IN_SITE, NotificationChannel.EMAIL]
        )


# 全局通知管理器
notification_manager = NotificationManager()