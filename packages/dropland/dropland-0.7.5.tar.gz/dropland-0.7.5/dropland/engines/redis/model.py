import asyncio
import contextlib
import enum
from datetime import timedelta
from typing import Any, Optional

from dropland.data.context import get_context
from dropland.data.models.cache import MethodCache
from dropland.data.models.nosql import NoSqlModel, NoSqlProxyModel
from dropland.data.serializers import Serializer, Deserializer
from dropland.data.serializers.pickle import PickleSerializer, PickleDeserializer
from .engine import RedisEngine


class RedisCacheType(int, enum.Enum):
    SIMPLE = 0
    HASH = 1


class RedisModel(NoSqlModel):
    class Meta(NoSqlModel.Meta):
        _redis_engine = None

    def __init_subclass__(
            cls, redis_engine: RedisEngine = None,
            cache_type: RedisCacheType = RedisCacheType.SIMPLE,
            serializer: Optional[Serializer] = None,
            deserializer: Optional[Deserializer] = None,
            ttl_enabled: bool = True,
            **kwargs):
        from .cache import SimpleRedisModelCache, HashRedisModelCache

        if not redis_engine:
            return super().__init_subclass__(**kwargs)

        serializer = serializer or PickleSerializer()
        deserializer = deserializer or PickleDeserializer()

        protocol_class = SimpleRedisModelCache \
            if cache_type == RedisCacheType.SIMPLE \
            else HashRedisModelCache

        cache_protocol = protocol_class(
            redis_engine, cls.__name__,
            serializer, deserializer,
            ttl_enabled=ttl_enabled
        )

        cls.Meta._redis_engine = redis_engine

        super().__init_subclass__(
            cache_protocol=cache_protocol,
            serializer=serializer,
            deserializer=deserializer,
            **kwargs
        )

    def get_id_value(self) -> Any:
        raise NotImplementedError

    # noinspection PyProtectedMember
    @classmethod
    def get_engine(cls) -> 'RedisEngine':
        return cls.Meta._redis_engine

    @classmethod
    @contextlib.asynccontextmanager
    async def _session_context(cls):
        ctx = get_context()

        if '_redis_cond' not in ctx:
            ctx._redis_cnt = 0
            ctx._redis_cond = asyncio.Condition()

        async with ctx._redis_cond:
            if 'redis' in ctx:
                ctx._redis_cnt += 1
                ctx._redis_cond.release()
                try:
                    yield ctx
                finally:
                    await ctx._redis_cond.acquire()
                    ctx._redis_cnt -= 1
                    if 0 == ctx._redis_cnt:
                        ctx._redis_cond.notify()
            else:
                async with cls.get_engine().session() as session:
                    ctx.redis = session
                    assert ctx.redis
                    ctx._redis_cnt = 1
                    ctx._redis_cond.release()
                    try:
                        yield ctx
                    finally:
                        await ctx._redis_cond.acquire()
                        ctx._redis_cnt -= 1
                        if 0 == ctx._redis_cnt:
                            del ctx.redis
                        else:
                            await ctx._redis_cond.wait_for(lambda: 0 == ctx._redis_cnt)
                            del ctx.redis


class RedisProxyModel(NoSqlProxyModel, RedisModel):
    class Meta(NoSqlProxyModel.Meta, RedisModel.Meta):
        pass

    def __init_subclass__(cls, redis_engine: RedisEngine = None, **kwargs):
        super().__init_subclass__(redis_engine=redis_engine, **kwargs)
        cls.Meta._redis_engine = redis_engine

    def get_id_value(self) -> Any:
        raise NotImplementedError


class RedisMethodCache(MethodCache):
    def __init__(
            self, redis_engine: RedisEngine, model_name: str,
            cache_type: RedisCacheType = RedisCacheType.SIMPLE,
            serializer: Optional[Serializer] = None,
            deserializer: Optional[Deserializer] = None,
            ttl: Optional[timedelta] = None):
        from .cache import SimpleRedisModelCache, HashRedisModelCache

        serializer = serializer or PickleSerializer()
        deserializer = deserializer or PickleDeserializer()

        protocol_class = SimpleRedisModelCache \
            if cache_type == RedisCacheType.SIMPLE \
            else HashRedisModelCache

        cache_protocol = protocol_class(
            redis_engine, model_name,
            serializer, deserializer,
            ttl_enabled=True
        )

        super().__init__(cache_protocol, ttl)
        self._redis_engine = redis_engine
        self._cache_type = cache_type

    @contextlib.asynccontextmanager
    async def _session_context(self):
        ctx = get_context()

        if '_redis_cond' not in ctx:
            ctx._redis_cnt = 0
            ctx._redis_cond = asyncio.Condition()

        async with ctx._redis_cond:
            if 'redis' in ctx:
                ctx._redis_cnt += 1
                ctx._redis_cond.release()
                try:
                    yield ctx
                finally:
                    await ctx._redis_cond.acquire()
                    ctx._redis_cnt -= 1
                    if 0 == ctx._redis_cnt:
                        ctx._redis_cond.notify()
            else:
                async with self._redis_engine.session() as session:
                    ctx.redis = session
                    assert ctx.redis
                    ctx._redis_cnt = 1
                    ctx._redis_cond.release()
                    try:
                        yield ctx
                    finally:
                        await ctx._redis_cond.acquire()
                        ctx._redis_cnt -= 1
                        if 0 == ctx._redis_cnt:
                            del ctx.redis
                        else:
                            await ctx._redis_cond.wait_for(lambda: 0 == ctx._redis_cnt)
                            del ctx.redis
