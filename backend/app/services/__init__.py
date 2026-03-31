"""
服务层模块
"""
from app.services.price_compare import engine, PriceCompareEngine, PriceItem, CompareResult
from app.services.price_cache import price_cache, PriceCache
from app.services.platforms import zkh_adapter, western_adapter, jd_adapter

__all__ = [
    "engine",
    "PriceCompareEngine",
    "PriceItem", 
    "CompareResult",
    "price_cache",
    "PriceCache",
    "zkh_adapter",
    "western_adapter",
    "jd_adapter"
]