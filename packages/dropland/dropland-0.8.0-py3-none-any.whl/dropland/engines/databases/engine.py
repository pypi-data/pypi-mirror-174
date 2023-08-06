import asyncio
from collections import defaultdict
from contextlib import asynccontextmanager, AbstractAsyncContextManager
from dataclasses import dataclass, replace
from typing import Dict, Set, Optional, List, Mapping, Callable, Any

from databases.core import Database, Connection

from dropland.engines.base import EngineBackend, AsyncEngine
from dropland.engines.sql import SqlEngineType
from dropland.log import tr, logger


@dataclass
class EngineConfig:
    url: str
    echo: bool = False
    pool_min_size: int = 1
    pool_max_size: int = 8
    pool_expire_seconds: int = 60


class DbEngineBackend(EngineBackend):
    def __init__(self):
        self._engines: Dict[str, 'DbEngine'] = dict()
        self._engines_by_type: Dict[SqlEngineType, Set[str]] = defaultdict(set)

    @property
    def name(self) -> str:
        return 'db'

    # noinspection PyMethodOverriding
    def create_engine(self, name: str, config: EngineConfig, db_type: SqlEngineType) -> 'DbEngine':
        if engine := self._engines.get(name):
            return engine

        uri = config.url
        params = dict()

        if db_type == SqlEngineType.SQLITE:
            uri = uri.replace('sqlite', 'sqlite+aiosqlite', 1)
        elif db_type == SqlEngineType.POSTGRES:
            uri = uri.replace('postgresql', 'postgresql+asyncpg', 1)
            params.update(dict(
                min_size=config.pool_min_size,
                max_size=config.pool_max_size,
                max_inactive_connection_lifetime=config.pool_expire_seconds,
            ))
        elif db_type == SqlEngineType.MYSQL:
            uri = uri.replace('mysql', 'mysql+aiomysql', 1)
            params.update(dict(
                echo=config.echo,
                minsize=config.pool_min_size,
                maxsize=config.pool_max_size,
                pool_recycle=config.pool_expire_seconds,
            ))

        config = replace(config, url=uri)
        engine = DbEngine(self, name, db_type, config, params)
        self._engines[name] = engine
        self._engines_by_type[db_type].add(name)
        logger.info(tr('dropland.engines.db.engine.created').format(name=name, db_type=db_type))
        return engine

    def get_engine(self, name: str) -> Optional['DbEngine']:
        return self._engines.get(name)

    def get_engine_names(self) -> List[str]:
        return list(self._engines.keys())

    def get_engines_for_type(self, db_type: SqlEngineType) -> List['DbEngine']:
        engine_names = self._engines_by_type[db_type]
        return [self.get_engine(name) for name in engine_names]

    def get_engines(self, names: Optional[List[str]] = None) -> Mapping[str, 'DbEngine']:
        engines = dict()

        if not names:
            names = self.get_engine_names()

        for name in names:
            if engine := self.get_engine(name):
                engines[name] = engine

        return engines


class DbEngine(AsyncEngine[Connection]):
    def __init__(self, backend: DbEngineBackend, name: str, db_type: SqlEngineType,
                 config: EngineConfig, params: Dict[str, Any]):
        super().__init__(backend)
        self._name = name
        self._db_type = db_type
        self._db = Database(config.url, **params)
        self._lock = asyncio.Lock()
        self._counter = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def db_type(self):
        return self._db_type

    @asynccontextmanager
    async def session(self, begin_tx: bool = True, force_rollback: bool = False) \
            -> Callable[..., AbstractAsyncContextManager[Connection]]:
        async with self._db.connection() as conn:
            if begin_tx:
                async with conn.transaction(force_rollback=force_rollback):
                    yield conn
            else:
                yield conn

    async def start(self):
        async with self._lock:
            if 0 == self._counter:
                await self._db.connect()
                logger.info(tr('dropland.engines.db.engine.started').format(name=self.name, db_type=self.db_type))
            self._counter += 1

    async def stop(self):
        async with self._lock:
            if 1 == self._counter:
                await self._db.disconnect()
                logger.info(tr('dropland.engines.db.engine.stopped').format(name=self.name, db_type=self.db_type))
            self._counter = max(self._counter - 1, 0)
