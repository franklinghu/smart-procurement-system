"""
价格 API - 比价引擎接口
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from app.services.price_compare import engine, CompareResult
from app.services.platforms import zkh_adapter, western_adapter, jd_adapter
from app.services.price_cache import price_cache
from app.core.security import get_current_tenant_id

# 注册平台适配器
engine.register_adapter(zkh_adapter)
engine.register_adapter(western_adapter)
engine.register_adapter(jd_adapter)

router = APIRouter()


# ============ Schema ============

class CompareRequest(BaseModel):
    """比价请求"""
    keyword: str
    platforms: Optional[List[str]] = None
    use_cache: bool = True


class PriceItemResponse(BaseModel):
    """价格项响应"""
    platform: str
    platform_id: str
    goods_name: str
    goods_spec: str
    sku_code: str
    price: float
    original_price: float
    discount_rate: float
    stock_status: str
    stock_quantity: int
    moq: int
    delivery_days: int
    delivery_place: str
    platform_url: str
    supplier_name: str


class CompareResponse(BaseModel):
    """比价响应"""
    task_id: str
    goods_keyword: str
    items: List[PriceItemResponse]
    best_price: Optional[PriceItemResponse]
    compare_time: str
    status: str
    from_cache: bool = False


class RefreshRequest(BaseModel):
    """刷新价格请求"""
    keyword: str
    platforms: Optional[List[str]] = None


# ============ API 接口 ============

@router.post("/compare", response_model=CompareResponse)
async def compare_prices(
    request: CompareRequest,
    tenant_id: UUID = Query(None)
):
    """
    发起比价
    
    - keyword: 搜索关键词（商品名称）
    - platforms: 指定平台列表，如 ["zkh", "western", "jd"]
    - use_cache: 是否使用缓存
    """
    # 平台过滤
    available_platforms = ["zkh", "western", "jd"]
    platforms = request.platforms or available_platforms
    
    # 检查缓存
    if request.use_cache:
        cached_items = price_cache.get(request.keyword, platforms)
        if cached_items:
            best = engine._calculate_best(cached_items) if cached_items else None
            
            return CompareResponse(
                task_id="cached",
                goods_keyword=request.keyword,
                items=[PriceItemResponse(
                    platform=i.platform,
                    platform_id=i.platform_id,
                    goods_name=i.goods_name,
                    goods_spec=i.goods_spec,
                    sku_code=i.sku_code,
                    price=i.price,
                    original_price=i.original_price,
                    discount_rate=i.discount_rate,
                    stock_status=i.stock_status,
                    stock_quantity=i.stock_quantity,
                    moq=i.moq,
                    delivery_days=i.delivery_days,
                    delivery_place=i.delivery_place,
                    platform_url=i.platform_url,
                    supplier_name=i.supplier_name
                ) for i in cached_items],
                best_price=PriceItemResponse(
                    platform=best.platform,
                    platform_id=best.platform_id,
                    goods_name=best.goods_name,
                    goods_spec=best.goods_spec,
                    sku_code=best.sku_code,
                    price=best.price,
                    original_price=best.original_price,
                    discount_rate=best.discount_rate,
                    stock_status=best.stock_status,
                    stock_quantity=best.stock_quantity,
                    moq=best.moq,
                    delivery_days=best.delivery_days,
                    delivery_place=best.delivery_place,
                    platform_url=best.platform_url,
                    supplier_name=best.supplier_name
                ) if best else None,
                compare_time=cached_items[0].__dict__.get('compare_time', '').isoformat() if hasattr(cached_items[0], 'compare_time') else '',
                status="success",
                from_cache=True
            )
    
    # 执行比价
    result = await engine.compare(request.keyword, platforms)
    
    # 存入缓存
    if result.items:
        price_cache.set(request.keyword, platforms, result.items)
    
    return CompareResponse(
        task_id=result.task_id,
        goods_keyword=result.goods_keyword,
        items=[PriceItemResponse(
            platform=i.platform,
            platform_id=i.platform_id,
            goods_name=i.goods_name,
            goods_spec=i.goods_spec,
            sku_code=i.sku_code,
            price=i.price,
            original_price=i.original_price,
            discount_rate=i.discount_rate,
            stock_status=i.stock_status,
            stock_quantity=i.stock_quantity,
            moq=i.moq,
            delivery_days=i.delivery_days,
            delivery_place=i.delivery_place,
            platform_url=i.platform_url,
            supplier_name=i.supplier_name
        ) for i in result.items],
        best_price=PriceItemResponse(
            platform=result.best_price.platform,
            platform_id=result.best_price.platform_id,
            goods_name=result.best_price.goods_name,
            goods_spec=result.best_price.goods_spec,
            sku_code=result.best_price.sku_code,
            price=result.best_price.price,
            original_price=result.best_price.original_price,
            discount_rate=result.best_price.discount_rate,
            stock_status=result.best_price.stock_status,
            stock_quantity=result.best_price.stock_quantity,
            moq=result.best_price.moq,
            delivery_days=result.best_price.delivery_days,
            delivery_place=result.best_price.delivery_place,
            platform_url=result.best_price.platform_url,
            supplier_name=result.best_price.supplier_name
        ) if result.best_price else None,
        compare_time=result.compare_time.isoformat(),
        status=result.status,
        from_cache=False
    )


@router.post("/refresh", response_model=CompareResponse)
async def refresh_prices(
    request: RefreshRequest,
    tenant_id: UUID = Query(None)
):
    """强制刷新价格（绕过缓存）"""
    platforms = request.platforms or ["zkh", "western", "jd"]
    
    # 清除缓存
    price_cache.invalidate(request.keyword, platforms)
    
    # 重新比价
    result = await engine.compare(request.keyword, platforms)
    
    # 存入缓存
    if result.items:
        price_cache.set(request.keyword, platforms, result.items)
    
    return CompareResponse(
        task_id=result.task_id,
        goods_keyword=result.goods_keyword,
        items=[PriceItemResponse(
            platform=i.platform,
            platform_id=i.platform_id,
            goods_name=i.goods_name,
            goods_spec=i.goods_spec,
            sku_code=i.sku_code,
            price=i.price,
            original_price=i.original_price,
            discount_rate=i.discount_rate,
            stock_status=i.stock_status,
            stock_quantity=i.stock_quantity,
            moq=i.moq,
            delivery_days=i.delivery_days,
            delivery_place=i.delivery_place,
            platform_url=i.platform_url,
            supplier_name=i.supplier_name
        ) for i in result.items],
        best_price=PriceItemResponse(
            platform=result.best_price.platform,
            platform_id=result.best_price.platform_id,
            goods_name=result.best_price.goods_name,
            goods_spec=result.best_price.goods_spec,
            sku_code=result.best_price.sku_code,
            price=result.best_price.price,
            original_price=result.best_price.original_price,
            discount_rate=result.best_price.discount_rate,
            stock_status=result.best_price.stock_status,
            stock_quantity=result.best_price.stock_quantity,
            moq=result.best_price.moq,
            delivery_days=result.best_price.delivery_days,
            delivery_place=result.best_price.delivery_place,
            platform_url=result.best_price.platform_url,
            supplier_name=result.best_price.supplier_name
        ) if result.best_price else None,
        compare_time=result.compare_time.isoformat(),
        status=result.status,
        from_cache=False
    )


@router.get("/cache/stats")
async def get_cache_stats():
    """获取缓存状态"""
    return price_cache.get_stats()


@router.delete("/cache")
async def clear_cache(keyword: str = Query(None)):
    """清除缓存"""
    price_cache.invalidate(keyword)
    return {"message": "缓存已清除"}