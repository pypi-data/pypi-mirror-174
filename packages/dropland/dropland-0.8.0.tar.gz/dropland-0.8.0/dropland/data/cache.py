from dataclasses import dataclass
from datetime import timedelta
from typing import Protocol, Any, List, Optional, Dict, Tuple, AsyncContextManager


@dataclass
class ModelCacheData:
    cache_id: str
    data: Optional[Any] = None


class ModelCacheProtocol(Protocol):
    def get_model_cache_key(self) -> str:
        ...

    def get_cache_id(self, id_value: Any) -> str:
        return str(id_value)

    def get_cache_key(self, id_value: Any) -> str:
        return f'{self.get_model_cache_key()}:{self.get_cache_id(id_value)}'

    async def cache_one(
            self, session, data: ModelCacheData, ttl: Optional[timedelta] = None, **kwargs) -> bool:
        ...

    async def cache_many(
            self, session, objects: List[ModelCacheData], ttl: Optional[timedelta] = None, **kwargs) -> bool:
        ...

    async def load_one(
            self, session, cache_key: str, **kwargs) -> Tuple[bool, Optional[Any]]:
        ...

    async def load_many(
            self, session, indices: List[Any], **kwargs) -> List[Optional[Dict[str, Any]]]:
        ...

    async def drop_one(self, session, cache_key: str) -> bool:
        ...

    async def drop_many(self, session, indices: List[Any] = None) -> int:
        ...

    async def drop_all(self, session, prefix: Optional[str] = None) -> int:
        ...

    async def exists(self, session, cache_key: str) -> bool:
        ...

    async def scan(
        self, session, cache_key: str = None,
            match: str = None, count: int = None) -> AsyncContextManager[Tuple[str, Optional[Dict[str, Any]]]]:
        ...
