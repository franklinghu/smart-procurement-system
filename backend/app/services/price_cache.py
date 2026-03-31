"""
价格缓存服务
"""
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from app.services.price_compare import PriceItem


class PriceCache:
    """价格缓存"""
    
    def __init__(self, ttl_seconds: int = 3600):  # 默认1小时
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict] = {}
    
    def _make_key(self, keyword: str, platforms: List[str]) -> str:
        """生成缓存key"""
        platform_key = "_".join(sorted(platforms))
        return f"{keyword}:{platform_key}"
    
    def get(self, keyword: str, platforms: List[str]) -> Optional[List[PriceItem]]:
        """获取缓存"""
        key = self._make_key(keyword, platforms)
        
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        
        # 检查是否过期
        if (datetime.now() - cache_entry['timestamp']).seconds > self.ttl_seconds:
            del self._cache[key]
            return None
        
        return cache_entry['items']
    
    def set(self, keyword: str, platforms: List[str], items: List[PriceItem]):
        """设置缓存"""
        key = self._make_key(keyword, platforms)
        self._cache[key] = {
            'items': items,
            'timestamp': datetime.now()
        }
    
    def invalidate(self, keyword: str = None, platforms: List[str] = None):
        """清除缓存"""
        if keyword is None and platforms is None:
            # 清除所有
            self._cache.clear()
        elif keyword and platforms:
            # 清除指定
            key = self._make_key(keyword, platforms)
            if key in self._cache:
                del self._cache[key]
        elif keyword:
            # 清除指定关键词的所有
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(f"{keyword}:")]
            for k in keys_to_delete:
                del self._cache[k]
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        total = len(self._cache)
        expired = 0
        
        for entry in self._cache.values():
            if (datetime.now() - entry['timestamp']).seconds > self.ttl_seconds:
                expired += 1
        
        return {
            'total': total,
            'valid': total - expired,
            'expired': expired
        }


# 全局缓存实例
price_cache = PriceCache()