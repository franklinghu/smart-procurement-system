"""
ERP 对接模块 - 用友U8适配器
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json


class SyncStatus(str, Enum):
    """同步状态"""
    PENDING = "pending"
    SYNCING = "syncing"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class PurchaseOrder:
    """采购订单"""
    order_id: str
    order_no: str
    tenant_id: str
    supplier_id: str
    supplier_name: str
    total_amount: float
    payment_method: str
    delivery_place: str
    items: List[Dict]
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class ERPSyncRecord:
    """ERP同步记录"""
    id: str
    order_id: str
    order_no: str
    erp_order_id: Optional[str]
    erp_order_no: Optional[str]
    status: SyncStatus
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    synced_at: Optional[datetime]


class BaseERPAdapter(ABC):
    """ERP适配器基类"""
    
    erp_name: str = ""
    erp_code: str = ""
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """测试连接"""
        pass
    
    @abstractmethod
    async def create_purchase_order(self, order: PurchaseOrder) -> Dict:
        """创建采购订单"""
        pass
    
    @abstractmethod
    async def get_order_status(self, erp_order_id: str) -> Dict:
        """获取订单状态"""
        pass
    
    @abstractmethod
    async def cancel_order(self, erp_order_id: str) -> bool:
        """取消订单"""
        pass


class YongyouU8Adapter(BaseERPAdapter):
    """用友U8 ERP适配器"""
    
    erp_name = "用友U8"
    erp_code = "yongyou_u8"
    
    def __init__(self, host: str, app_id: str, app_key: str, user: str, password: str):
        self.host = host
        self.app_id = app_id
        self.app_key = app_key
        self.user = user
        self.password = password
    
    async def test_connection(self) -> bool:
        """测试连接"""
        # 模拟API调用
        # 实际项目中调用用友U8 WebService
        return True
    
    async def create_purchase_order(self, order: PurchaseOrder) -> Dict:
        """
        创建采购订单
        调用用友U8的采购订单API
        """
        # 构建U8格式的采购订单
        u8_order = {
            "Head": {
                "ccode": order.order_no,  # 单据号
                "ddate": order.created_at.strftime("%Y-%m-%d"),  # 日期
                "cvouchtype": "01",  # 采购订单
                "cvencode": self._get_supplier_code(order.supplier_id),  # 供应商编码
                "cmaker": self.user,  # 制单人
                "cmemo": "智能工业品采购系统自动创建",  # 备注
            },
            "Body": []
        }
        
        # 转化明细行
        for idx, item in enumerate(order.items, 1):
            u8_order["Body"].append({
                "cinvcode": item.get("goods_code", ""),  # 存货编码
                "cinvname": item.get("goods_name", ""),  # 存货名称
                "cinvstd": item.get("spec", ""),  # 规格型号
                "inum": item.get("quantity", 0),  # 数量
                "iprice": item.get("price", 0),  # 单价
                "itaxprice": item.get("price", 0) * 1.13,  # 含税单价
                "itax": item.get("price", 0) * 0.13,  # 税额
                "isum": item.get("quantity", 0) * item.get("price", 0),  # 价税合计
            })
        
        # 模拟API调用
        # response = await self._call_api("/api/purchase/order/create", u8_order)
        
        # 返回模拟结果
        return {
            "success": True,
            "erp_order_id": f"U8-{order.order_no}",
            "erp_order_no": order.order_no,
            "message": "订单创建成功"
        }
    
    async def get_order_status(self, erp_order_id: str) -> Dict:
        """获取订单状态"""
        # 模拟API调用
        return {
            "erp_order_id": erp_order_id,
            "status": "approved",
            "message": "订单已审核"
        }
    
    async def cancel_order(self, erp_order_id: str) -> bool:
        """取消订单"""
        # 模拟API调用
        return True
    
    def _get_supplier_code(self, supplier_id: str) -> str:
        """获取供应商编码"""
        # 实际项目中查询映射表
        return f"SUP-{supplier_id[:8]}"


class ERPManager:
    """ERP管理器"""
    
    def __init__(self):
        self.adapters: Dict[str, BaseERPAdapter] = {}
        self.sync_records: Dict[str, ERPSyncRecord] = {}
    
    def register_adapter(self, adapter: BaseERPAdapter):
        """注册ERP适配器"""
        self.adapters[adapter.erp_code] = adapter
    
    async def sync_order(self, order: PurchaseOrder, erp_code: str = "yongyou_u8") -> ERPSyncRecord:
        """同步订单到ERP"""
        adapter = self.adapters.get(erp_code)
        if not adapter:
            raise ValueError(f"ERP适配器 {erp_code} 未注册")
        
        # 创建同步记录
        record = ERPSyncRecord(
            id=f"sync-{order.order_id}",
            order_id=order.order_id,
            order_no=order.order_no,
            erp_order_id=None,
            erp_order_no=None,
            status=SyncStatus.SYNCING,
            error_message=None,
            retry_count=0,
            created_at=datetime.now(),
            synced_at=None
        )
        
        try:
            # 调用ERP创建订单
            result = await adapter.create_purchase_order(order)
            
            if result.get("success"):
                record.status = SyncStatus.SUCCESS
                record.erp_order_id = result.get("erp_order_id")
                record.erp_order_no = result.get("erp_order_no")
                record.synced_at = datetime.now()
            else:
                record.status = SyncStatus.FAILED
                record.error_message = result.get("message", "创建失败")
                
        except Exception as e:
            record.status = SyncStatus.FAILED
            record.error_message = str(e)
        
        self.sync_records[record.id] = record
        return record
    
    async def retry_sync(self, sync_id: str) -> ERPSyncRecord:
        """重试同步"""
        record = self.sync_records.get(sync_id)
        if not record:
            raise ValueError("同步记录不存在")
        
        record.retry_count += 1
        record.status = SyncStatus.SYNCING
        
        # 重新同步逻辑...
        
        return record
    
    def get_sync_records(self, order_id: str = None) -> List[ERPSyncRecord]:
        """获取同步记录"""
        if order_id:
            return [r for r in self.sync_records.values() if r.order_id == order_id]
        return list(self.sync_records.values())


# 全局ERP管理器
erp_manager = ERPManager()

# 注册默认适配器
_default_adapter = YongyouU8Adapter(
    host="http://u8-server:8088",
    app_id="procurement_app",
    app_key="app_key_xxx",
    user="admin",
    password="admin123"
)
erp_manager.register_adapter(_default_adapter)