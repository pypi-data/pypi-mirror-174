import asyncio
from contextlib import asynccontextmanager, AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Mapping, Optional, Callable

from aioredis import ConnectionsPool, Redis, create_pool

from dropland.log import logger, tr
from ..base import EngineBackend, AsyncEngine

Connection = Redis


@dataclass
class EngineConfig:
    url: str
    max_connections: int = 4
    pool_timeout_seconds: int = 5


class RedisEngineBackend(EngineBackend):
    def __init__(self):
        self._engines: Dict[str, 'RedisEngine'] = dict()

    @property
    def name(self) -> str:
        return 'redis'

    # noinspection PyMethodOverriding
    def create_engine(self, name: str, config: EngineConfig,
                      default_ttl: timedelta = timedelta(seconds=60)) -> 'RedisEngine':
        if engine := self._engines.get(name):
            return engine

        engine = RedisEngine(self, name, config, default_ttl)
        self._engines[name] = engine
        logger.info(tr('dropland.engines.redis.engine.created').format(name=name))
        return engine

    def get_engine(self, name: str) -> Optional['RedisEngine']:
        return self._engines.get(name)

    def get_engine_names(self) -> List[str]:
        return list(self._engines.keys())

    def get_engines(self, names: Optional[List[str]] = None) -> Mapping[str, 'RedisEngine']:
        engines = dict()

        if not names:
            names = self.get_engine_names()

        for name in names:
            if engine := self.get_engine(name):
                engines[name] = engine

        return engines


class RedisEngine(AsyncEngine[Connection]):
    def __init__(self, backend: RedisEngineBackend, name: str, config: EngineConfig, default_ttl: timedelta):
        super().__init__(backend)
        self._name = name
        self._config = config
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()
        self._pool: Optional[ConnectionsPool] = None
        self._counter = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_ttl(self) -> timedelta:
        return self._default_ttl

    @asynccontextmanager
    async def session(self, *args, **kwargs) -> Callable[..., AbstractAsyncContextManager[Connection]]:
        with await Redis(self._pool) as conn:
            yield conn

    async def start(self):
        async with self._lock:
            if 0 == self._counter:
                assert not self._pool
                self._pool = await create_pool(
                    self._config.url, create_connection_timeout=self._config.pool_timeout_seconds,
                    minsize=1, maxsize=self._config.max_connections
                )
                logger.info(tr('dropland.engines.redis.engine.started').format(name=self.name))

            self._counter += 1

    async def stop(self):
        async with self._lock:
            if 1 == self._counter:
                assert self._pool
                self._pool.close()
                await self._pool.wait_closed()
                self._pool = None
                logger.info(tr('dropland.engines.redis.engine.stopped').format(name=self.name))

            self._counter = max(self._counter - 1, 0)
