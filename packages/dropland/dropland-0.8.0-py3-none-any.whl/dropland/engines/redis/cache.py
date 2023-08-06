from collections import OrderedDict
from datetime import timedelta
from typing import Optional, Dict, Any, List, Tuple, AsyncContextManager

from dropland.data.cache import ModelCacheProtocol, ModelCacheData
from dropland.data.serializers import Serializer, Deserializer
from .engine import RedisEngine, Connection


class SimpleRedisModelCache(ModelCacheProtocol):
    def __init__(self, engine: RedisEngine, class_key: str,
                 serializer: Serializer, deserializer: Deserializer, ttl_enabled: bool = True):
        self._redis_engine = engine
        self._class_key = class_key
        self._serializer = serializer
        self._deserializer = deserializer
        self._ttl_enabled = ttl_enabled
        self._null_data = self._serializer.serialize(None)

    def get_model_cache_key(self) -> str:
        return f'{self._redis_engine.name}.models.{self._class_key}'

    async def cache_one(
            self, session: Connection, data: ModelCacheData, ttl: Optional[timedelta] = None, **kwargs) -> bool:
        cache_kwargs = dict()

        if self._ttl_enabled:
            expiration = ttl or self._redis_engine.default_ttl
            total_seconds = expiration.total_seconds()

            if total_seconds > 1:
                cache_kwargs['expire'] = int(total_seconds)
            elif 0 < total_seconds < 1:
                cache_kwargs['pexpire'] = int(total_seconds * 1000)
            else:
                total_seconds = self._redis_engine.default_ttl.total_seconds()
                cache_kwargs['expire'] = int(total_seconds) if total_seconds > 1 else 60

        serialized = self._serializer.serialize(data.data)
        return bool(await session.set(self.get_cache_key(data.cache_id), serialized, **cache_kwargs))

    async def cache_many(
            self, session: Connection, objects: List[ModelCacheData],
            ttl: Optional[timedelta] = None, **kwargs) -> bool:
        if not objects:
            return False
        res = False

        tx = session.multi_exec()

        for instance in objects:
            cache_kwargs = dict()

            if self._ttl_enabled:
                expiration = ttl or self._redis_engine.default_ttl
                total_seconds = expiration.total_seconds()

                if total_seconds > 1:
                    cache_kwargs['expire'] = int(total_seconds)
                elif 0 < total_seconds < 1:
                    cache_kwargs['pexpire'] = int(total_seconds * 1000)
                else:
                    total_seconds = self._redis_engine.default_ttl.total_seconds()
                    cache_kwargs['expire'] = int(total_seconds) if total_seconds > 1 else 60

            serialized = self._serializer.serialize(instance.data)
            tx.set(self.get_cache_key(instance.cache_id), serialized, **cache_kwargs)

        for r in await tx.execute():
            res |= r

        return bool(res)

    async def load_one(
            self, session: Connection, cache_key: str, **kwargs) -> Tuple[bool, Optional[Any]]:
        if res := await session.get(cache_key):
            return True, self._deserializer.deserialize(res)
        return False, None

    async def load_many(
            self, session: Connection, indices: List[Any], **kwargs) -> List[Optional[Dict[str, Any]]]:
        if not indices:
            return []

        cache_keys = [self.get_cache_key(id_value) for id_value in indices]
        res = await session.mget(*cache_keys)
        objects: Dict[Any, Any] = OrderedDict()

        for id_value, data in zip(indices, res):
            objects[id_value] = self._deserializer.deserialize(data) if data is not None else None

        return list(objects.values())

    async def drop_one(self, session: Connection, cache_key: str) -> bool:
        return bool(await session.delete(cache_key))

    async def drop_many(self, session: Connection, indices: List[Any] = None) -> int:
        if indices and len(indices) > 0:
            cache_keys = [self.get_cache_key(id_value) for id_value in indices]
        else:
            model_cache_key = self.get_model_cache_key()
            cache_keys = await session.keys(f'{model_cache_key}:*')

        return int(await session.delete(*cache_keys)) if cache_keys else 0

    async def drop_all(self, session: Connection, prefix: Optional[str] = None) -> int:
        model_cache_key = self.get_model_cache_key()
        cache_key = f'{model_cache_key}:{prefix}*' if prefix else f'{model_cache_key}:*'
        keys_to_delete = await session.keys(cache_key)
        return int(await session.delete(*keys_to_delete)) if keys_to_delete else 0

    async def exists(self, session: Connection, cache_key: str) -> bool:
        if await session.exists(cache_key):
            return await session.get(cache_key) != self._null_data
        return False

    async def scan(self, session: Connection, cache_key: str = None,
                   match: str = None, count: int = None) -> AsyncContextManager[Tuple[str, Optional[Dict[str, Any]]]]:
        match = f'{cache_key}:{match}' if cache_key and match else match
        async for k in session.iscan(match=match, count=count):
            cache_key = k.decode('utf-8')
            k = cache_key.split(':')[1] if ':' in cache_key else cache_key
            v = (await self.load_one(session, cache_key))[1]
            yield k, v


class HashRedisModelCache(ModelCacheProtocol):
    def __init__(self, engine: RedisEngine, class_key: str,
                 serializer: Serializer, deserializer: Deserializer, ttl_enabled: bool = True):
        self._redis_engine = engine
        self._class_key = class_key
        self._serializer = serializer
        self._deserializer = deserializer
        self._ttl_enabled = ttl_enabled
        self._null_data = self._serializer.serialize(None)

    def get_model_cache_key(self) -> str:
        return f'{self._redis_engine.name}.models.{self._class_key}'

    async def cache_one(
            self, session: Connection, data: ModelCacheData, ttl: Optional[timedelta] = None, **kwargs) -> bool:
        model_cache_key, cache_id = self.get_model_cache_key(), self.get_cache_id(data.cache_id)
        serialized = self._serializer.serialize(data.data)

        if self._ttl_enabled:
            res = False
            tx = session.multi_exec()
            expiration = ttl or self._redis_engine.default_ttl
            tx.hset(model_cache_key, cache_id, serialized)
            tx.expire(model_cache_key, int(expiration.total_seconds()))

            for r in await tx.execute():
                res |= r

            return bool(res)

        return bool(await session.hset(model_cache_key, cache_id, serialized))

    async def cache_many(
            self, session: Connection, objects: List[ModelCacheData],
            ttl: Optional[timedelta] = None, **kwargs) -> bool:
        if not objects:
            return False

        model_cache_key = self.get_model_cache_key()
        obj_dict = {
            self.get_cache_id(instance.cache_id): self._serializer.serialize(instance.data)
            for instance in objects
        }

        if self._ttl_enabled:
            res = False
            tx = session.multi_exec()
            expiration = ttl or self._redis_engine.default_ttl
            tx.hmset_dict(model_cache_key, obj_dict)
            tx.expire(model_cache_key, int(expiration.total_seconds()))

            for r in await tx.execute():
                res |= r

            return bool(res)

        return bool(await session.hmset_dict(model_cache_key, obj_dict))

    async def load_one(
            self, session: Connection, cache_key: str, **kwargs) -> Tuple[bool, Optional[Any]]:
        if ':' in cache_key:
            model_cache_key, cache_id = cache_key.split(':', maxsplit=1)
            if res := await session.hget(model_cache_key, cache_id):
                return True, self._deserializer.deserialize(res)
            return False, None
        else:
            if res := await session.get(cache_key):
                return True, self._deserializer.deserialize(res)
            return False, None

    async def load_many(
            self, session: Connection, indices: List[Any], **kwargs) -> List[Optional[Dict[str, Any]]]:
        if not indices:
            return []

        cache_keys = [self.get_cache_id(id_value) for id_value in indices]
        res = await session.hmget(self.get_model_cache_key(), *cache_keys)
        objects: Dict[Any, Any] = OrderedDict()

        for id_value, data in zip(indices, res):
            objects[id_value] = self._deserializer.deserialize(data) if data is not None else None

        return list(objects.values())

    async def drop_one(self, session: Connection, cache_key: str) -> bool:
        if ':' in cache_key:
            model_cache_key, cache_id = cache_key.split(':', maxsplit=1)
            return bool(await session.hdel(model_cache_key, cache_id))
        else:
            return bool(await session.delete(cache_key))

    async def drop_many(self, session: Connection, indices: List[Any] = None) -> int:
        model_cache_key = self.get_model_cache_key()

        if indices and len(indices) > 0:
            cache_keys = [self.get_cache_id(id_value) for id_value in indices]
        else:
            cache_keys = await session.hkeys(model_cache_key)

        return int(await session.hdel(model_cache_key, *cache_keys)) if cache_keys else 0

    async def drop_all(self, session: Connection, prefix: Optional[str] = None) -> int:
        model_cache_key = self.get_model_cache_key()
        if not prefix:
            keys_to_delete = await session.hkeys(model_cache_key)
        else:
            keys_to_delete = list()
            for cache_key in await session.hkeys(model_cache_key, encoding='ascii'):
                if cache_key.startswith(prefix):
                    keys_to_delete.append(cache_key)

        return int(await session.hdel(model_cache_key, *keys_to_delete)) if keys_to_delete else 0

    async def exists(self, session: Connection, cache_key: str) -> bool:
        if ':' in cache_key:
            model_cache_key, cache_id = cache_key.split(':', maxsplit=1)
            e = bool(await session.hexists(model_cache_key, cache_id))
        else:
            e = bool(await session.exists(cache_key))
        if e:
            return await session.get(cache_key) != self._null_data
        return False

    async def scan(self, session: Connection, cache_key: str = None,
                   match: str = None, count: int = None) -> AsyncContextManager[Tuple[str, Optional[Dict[str, Any]]]]:
        async for k, data in session.ihscan(cache_key, match=match, count=count):
            yield k.decode('utf-8'), self._deserializer.deserialize(data)
