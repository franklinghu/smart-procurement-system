"""
比价引擎 - 平台适配器基类
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio


@dataclass
class PriceItem:
    """价格项"""
    platform: str              # 平台标识
    platform_id: str          # 平台商品ID
    goods_name: str           # 商品名称
    goods_spec: str           # 规格型号
    sku_code: str             # SKU编码
    price: float              # 单价
    original_price: float     # 原价
    discount_rate: float      # 折扣率
    stock_status: str        # 库存状态
    stock_quantity: int       # 库存数量
    moq: int                  # 最小起订量
    delivery_days: int       # 交货天数
    delivery_place: str      # 交货地点
    platform_url: str        # 商品URL
    supplier_name: str        # 供应商/店铺名
    raw_data: Dict[str, Any] # 原始数据


@dataclass
class CompareResult:
    """比价结果"""
    task_id: str              # 任务ID
    goods_keyword: str        # 搜索关键词
    items: List[PriceItem]   # 价格列表
    best_price: Optional[PriceItem]  # 最优价格
    compare_time: datetime    # 比价时间
    status: str               # 状态：success/error/partial


class BasePlatformAdapter(ABC):
    """平台适配器基类"""
    
    platform_name: str = ""
    platform_code: str = ""
    
    def __init__(self):
        self.is_available = True
        self.last_error = None
        self.error_count = 0
    
    @abstractmethod
    async def search(self, keyword: str, **kwargs) -> List[PriceItem]:
        """搜索商品价格"""
        pass
    
    @abstractmethod
    async def get_detail(self, platform_id: str) -> Optional[PriceItem]:
        """获取商品详情"""
        pass
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            items = await self.search("测试", limit=1)
            return len(items) > 0
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def mark_error(self):
        """标记错误"""
        self.error_count += 1
        if self.error_count >= 3:
            self.is_available = False
    
    def mark_success(self):
        """标记成功"""
        self.error_count = 0
        self.is_available = True


class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed/open/half-open
    
    def call(self, func, *args, **kwargs):
        """执行函数，带熔断保护"""
        if self.state == "open":
            if self.last_failure_time and \
               (datetime.now() - self.last_failure_time).seconds > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise e


class PriceCompareEngine:
    """比价引擎"""
    
    def __init__(self):
        self.adapters: Dict[str, BasePlatformAdapter] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def register_adapter(self, adapter: BasePlatformAdapter):
        """注册平台适配器"""
        self.adapters[adapter.platform_code] = adapter
        self.circuit_breakers[adapter.platform_code] = CircuitBreaker()
    
    async def compare(self, keyword: str, platforms: List[str] = None) -> CompareResult:
        """并行比价"""
        import uuid
        
        if platforms is None:
            platforms = list(self.adapters.keys())
        
        tasks = []
        for platform in platforms:
            if platform in self.adapters:
                adapter = self.adapters[platform]
                cb = self.circuit_breakers.get(platform)
                
                if adapter.is_available:
                    tasks.append(self._search_with_circuit(platform, keyword, adapter, cb))
        
        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 收集有效结果
        all_items = []
        for result in results:
            if isinstance(result, list):
                all_items.extend(result)
        
        # 计算最优价格（综合评分：价格×0.5 + 交货×0.3 + 起订量×0.2）
        best_price = self._calculate_best(all_items) if all_items else None
        
        # 确定状态
        if not all_items:
            status = "error"
        elif len(all_items) < len(platforms):
            status = "partial"
        else:
            status = "success"
        
        return CompareResult(
            task_id=str(uuid.uuid4()),
            goods_keyword=keyword,
            items=all_items,
            best_price=best_price,
            compare_time=datetime.now(),
            status=status
        )
    
    async def _search_with_circuit(self, platform: str, keyword: str, 
                                    adapter: BasePlatformAdapter, 
                                    cb: CircuitBreaker) -> List[PriceItem]:
        """带熔断的搜索"""
        try:
            return await adapter.search(keyword)
        except Exception as e:
            adapter.mark_error()
            print(f"[{platform}] Search error: {e}")
            return []
    
    def _calculate_best(self, items: List[PriceItem]) -> Optional[PriceItem]:
        """计算综合最优"""
        if not items:
            return None
        
        best = None
        best_score = float('-inf')
        
        for item in items:
            # 综合评分算法：分数越高越好
            # 价格得分：100 - (price / max_price * 50)
            max_price = max(i.price for i in items) or 1
            price_score = 50 * (1 - item.price / max_price)
            
            # 交货得分：100 - (delivery_days / max_days * 30)
            max_days = max(i.delivery_days for i in items) or 1
            delivery_score = 30 * (1 - item.delivery_days / max_days)
            
            # 起订量得分：100 - (moq / max_moq * 20)
            max_moq = max(i.moq for i in items) or 1
            moq_score = 20 * (1 - item.moq / max_moq)
            
            score = price_score + delivery_score + moq_score
            
            if score > best_score:
                best_score = score
                best = item
        
        return best


# 全局比价引擎实例
engine = PriceCompareEngine()