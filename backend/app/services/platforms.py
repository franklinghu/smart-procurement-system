"""
震坤行 (ZKH) 平台适配器
"""
import asyncio
from typing import List
from app.services.price_compare import BasePlatformAdapter, PriceItem


class ZKHAdapter(BasePlatformAdapter):
    """震坤行平台适配器"""
    
    platform_name = "震坤行"
    platform_code = "zkh"
    
    def __init__(self, api_key: str = "", api_secret: str = ""):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
    
    async def search(self, keyword: str, **kwargs) -> List[PriceItem]:
        """
        搜索商品
        实际项目中这里会调用震坤行开放API
        """
        # 模拟API调用延迟
        await asyncio.sleep(0.5)
        
        # 模拟返回数据（实际项目中替换为真实API调用）
        items = [
            PriceItem(
                platform=self.platform_code,
                platform_id="ZKH001",
                goods_name=f"{keyword} - 震坤行商品A",
                goods_spec="标准规格",
                sku_code="SKU-ZKH-001",
                price=125.00,
                original_price=150.00,
                discount_rate=0.83,
                stock_status="in_stock",
                stock_quantity=1000,
                moq=1,
                delivery_days=3,
                delivery_place="上海",
                platform_url="https://www.zkh.com/product/001",
                supplier_name="震坤行官方旗舰店",
                raw_data={}
            ),
            PriceItem(
                platform=self.platform_code,
                platform_id="ZKH002",
                goods_name=f"{keyword} - 震坤行商品B",
                goods_spec="Pro规格",
                sku_code="SKU-ZKH-002",
                price=118.00,
                original_price=148.00,
                discount_rate=0.80,
                stock_status="in_stock",
                stock_quantity=500,
                moq=1,
                delivery_days=2,
                delivery_place="上海",
                platform_url="https://www.zkh.com/product/002",
                supplier_name="震坤行工业超市",
                raw_data={}
            ),
        ]
        
        return items
    
    async def get_detail(self, platform_id: str) -> PriceItem:
        """获取商品详情"""
        items = await self.search("商品")
        return items[0] if items else None


class WesternAdapter(BasePlatformAdapter):
    """西域 (Western) 平台适配器"""
    
    platform_name = "西域"
    platform_code = "western"
    
    def __init__(self, api_key: str = "", api_secret: str = ""):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
    
    async def search(self, keyword: str, **kwargs) -> List[PriceItem]:
        """搜索商品"""
        await asyncio.sleep(0.5)
        
        items = [
            PriceItem(
                platform=self.platform_code,
                platform_id="WEST001",
                goods_name=f"{keyword} - 西域商品A",
                goods_spec="标准规格",
                sku_code="SKU-WEST-001",
                price=130.00,
                original_price=155.00,
                discount_rate=0.84,
                stock_status="in_stock",
                stock_quantity=800,
                moq=1,
                delivery_days=4,
                delivery_place="上海",
                platform_url="https://www.west.com/product/001",
                supplier_name="西域MRO商城",
                raw_data={}
            ),
            PriceItem(
                platform=self.platform_code,
                platform_id="WEST002",
                goods_name=f"{keyword} - 西域商品B",
                goods_spec="豪华规格",
                sku_code="SKU-WEST-002",
                price=145.00,
                original_price=160.00,
                discount_rate=0.91,
                stock_status="low_stock",
                stock_quantity=50,
                moq=5,
                delivery_days=5,
                delivery_place="上海",
                platform_url="https://www.west.com/product/002",
                supplier_name="西域工控旗舰店",
                raw_data={}
            ),
        ]
        
        return items
    
    async def get_detail(self, platform_id: str) -> PriceItem:
        """获取商品详情"""
        items = await self.search("商品")
        return items[0] if items else None


class JDIndustrialAdapter(BasePlatformAdapter):
    """京东工业品平台适配器"""
    
    platform_name = "京东工业品"
    platform_code = "jd"
    
    def __init__(self, app_key: str = "", app_secret: str = ""):
        super().__init__()
        self.app_key = app_key
        self.app_secret = app_secret
    
    async def search(self, keyword: str, **kwargs) -> List[PriceItem]:
        """搜索商品"""
        await asyncio.sleep(0.5)
        
        items = [
            PriceItem(
                platform=self.platform_code,
                platform_id="JD001",
                goods_name=f"{keyword} - 京东工业品A",
                goods_spec="官方标配",
                sku_code="SKU-JD-001",
                price=138.00,
                original_price=168.00,
                discount_rate=0.82,
                stock_status="in_stock",
                stock_quantity=2000,
                moq=1,
                delivery_days=2,
                delivery_place="全国",
                platform_url="https://mall.jd.com/product/001",
                supplier_name="京东工业品官方旗舰店",
                raw_data={}
            ),
            PriceItem(
                platform=self.platform_code,
                platform_id="JD002",
                goods_name=f"{keyword} - 京东工业品B",
                goods_spec="增值套装",
                sku_code="SKU-JD-002",
                price=155.00,
                original_price=175.00,
                discount_rate=0.89,
                stock_status="in_stock",
                stock_quantity=1200,
                moq=1,
                delivery_days=1,
                delivery_place="全国",
                platform_url="https://mall.jd.com/product/002",
                supplier_name="京东工业品专营店",
                raw_data={}
            ),
        ]
        
        return items
    
    async def get_detail(self, platform_id: str) -> PriceItem:
        """获取商品详情"""
        items = await self.search("商品")
        return items[0] if items else None



# 全局平台适配器实例
zkh_adapter = ZKHAdapter()
western_adapter = WesternAdapter()
jd_adapter = JDIndustrialAdapter()