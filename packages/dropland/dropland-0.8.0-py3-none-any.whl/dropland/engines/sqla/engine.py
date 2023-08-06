import asyncio
import sys
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import contextmanager, asynccontextmanager, AbstractContextManager, AbstractAsyncContextManager
from dataclasses import dataclass, replace
from datetime import timedelta
from typing import Dict, List, Mapping, Optional, Set, Callable

import ujson
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.schema import MetaData

from dropland.data.context import get_context
from dropland.log import logger, tr
from ..base import EngineBackend, SyncEngine, AsyncEngine
from ..sql import NAMING_CONVENTION, SqlEngineType


@dataclass
class EngineConfig:
    url: str
    echo: bool = False
    pool_min_size: int = 1
    pool_max_size: int = 8
    pool_expire_seconds: int = 60
    pool_timeout_seconds: int = 15


@dataclass
class EngineKey:
    db_type: SqlEngineType
    is_async: bool

    def __eq__(self, other: 'EngineKey'):
        return (self.db_type, self.is_async) == (other.db_type, other.is_async)

    def __hash__(self):
        return hash((self.db_type, self.is_async))


@dataclass
class EngineWithDbType:
    db_type: SqlEngineType
    engine: 'SqlEngine'


class SqlEngineBackend(EngineBackend):
    def __init__(self):
        self._engines: Dict[str, 'SqlEngine'] = dict()
        self._engines_by_key: Dict[EngineKey, Set[str]] = defaultdict(set)
        self._engines_by_type: Dict[SqlEngineType, Set[str]] = defaultdict(set)

    @property
    def name(self) -> str:
        return 'sqla'

    # noinspection PyMethodOverriding
    def create_engine(self, name: str, config: EngineConfig, db_type: SqlEngineType, use_async: bool) -> 'SqlEngine':
        if engine := self._engines.get(name):
            return engine

        uri = config.url

        if use_async:
            if db_type == SqlEngineType.SQLITE:
                uri = uri.replace('sqlite', 'sqlite+aiosqlite', 1)
            elif db_type == SqlEngineType.POSTGRES:
                uri = uri.replace('postgresql', 'postgresql+asyncpg', 1)
            elif db_type == SqlEngineType.MYSQL:
                uri = uri.replace('mysql', 'mysql+aiomysql', 1)
        else:
            if db_type == SqlEngineType.MYSQL:
                uri = uri.replace('mysql', 'mysql+pymysql', 1)

        config = replace(config, url=uri)

        params = dict(
            echo=config.echo,
            echo_pool=config.echo,
            pool_pre_ping=True,
            pool_recycle=config.pool_expire_seconds,
            json_serializer=ujson.dumps,
            json_deserializer=ujson.loads,
        )

        if db_type in (SqlEngineType.POSTGRES, SqlEngineType.MYSQL):
            params.update(dict(
                pool_size=config.pool_min_size,
                max_overflow=config.pool_max_size - config.pool_min_size,
                pool_timeout=config.pool_timeout_seconds
            ))

        if use_async:
            engine = create_async_engine(config.url, **params)
            session_factory = sessionmaker(engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)
        else:
            engine = create_sync_engine(config.url, **params)
            session_factory = sessionmaker(engine, autoflush=False)

        logger.info(tr('dropland.engines.sql.engine.created')
                    .format(name=self.name, db_type=db_type, async_=f'async={use_async}'))
        metadata = MetaData(bind=engine, naming_convention=NAMING_CONVENTION)
        engine_class = SqlAlchemyAsyncEngine if use_async else SqlAlchemySyncEngine

        engine = engine_class(
            self, name, engine, metadata, db_type, session_factory,
            timedelta(seconds=config.pool_timeout_seconds)
        )

        self._engines[name] = engine
        self._engines_by_key[EngineKey(db_type=db_type, is_async=use_async)].add(name)
        self._engines_by_type[db_type].add(name)
        return engine

    def get_engine(self, name: str) -> Optional['SqlEngine']:
        return self._engines.get(name)

    def get_engine_names(self) -> List[str]:
        return list(self._engines.keys())

    def get_engines_for_type(self, db_type: SqlEngineType, is_async: bool) -> List['SqlEngine']:
        engine_names = self._engines_by_key[EngineKey(db_type=db_type, is_async=is_async)]
        return [self.get_engine(name) for name in engine_names]

    def get_engines(self, names: Optional[List[str]] = None) -> Mapping[str, 'SqlEngine']:
        engines = dict()

        if not names:
            names = self.get_engine_names()

        for name in names:
            if engine := self.get_engine(name):
                engines[name] = engine

        return engines


class SqlEngine(ABC):
    def __init__(self, name: str, raw_engine, metadata, db_type: SqlEngineType, timeout: timedelta):
        self._name = name
        self._db_type = db_type
        self._timeout = timeout
        self._metadata = metadata
        self._engine = raw_engine.execution_options(timeout=int(timeout.total_seconds()))

    @property
    def name(self) -> str:
        return self._name

    @property
    def raw_engine(self):
        return self._engine

    @property
    def db_type(self):
        return self._db_type

    @property
    def timeout(self) -> timedelta:
        return self._timeout

    @property
    def metadata(self):
        return self._metadata

    @property
    @abstractmethod
    def connection_class(self):
        ...


class SqlAlchemySyncEngine(SyncEngine[Session], SqlEngine):
    def __init__(self, backend: SqlEngineBackend, name: str, engine, metadata,
                 db_type: SqlEngineType, session_factory, timeout: timedelta):
        SyncEngine.__init__(self, backend)
        SqlEngine.__init__(self, name, engine, metadata, db_type, timeout)

        self._session_factory = scoped_session(
            session_factory, scopefunc=lambda: get_context().session_id
        )
        self._lock = threading.Lock()
        self._counter = 0

    @property
    def connection_class(self):
        return Session

    @contextmanager
    def session(self, begin_tx: bool = True, force_rollback: bool = False) \
            -> Callable[..., AbstractContextManager[Session]]:
        if self._session_factory.registry.has():
            yield self._session_factory()
            return

        session: Session = self._session_factory()

        if begin_tx:
            with session.begin() as tx:
                yield session

                if sys.exc_info()[0] or force_rollback:
                    tx.rollback()
                else:
                    tx.commit()
        else:
            yield session

    def teardown_session(self):
        self._session_factory.remove()

    def start(self):
        with self._lock:
            if 0 == self._counter:
                logger.info(tr('dropland.engines.sql.engine.started')
                            .format(name=self.name, db_type=self.db_type, async_=f'async=False'))
            self._counter += 1

    def stop(self):
        with self._lock:
            if 1 == self._counter:
                self.raw_engine.dispose()
                logger.info(tr('dropland.engines.sql.engine.stopped')
                            .format(name=self.name, db_type=self.db_type, async_=f'async=False'))
            self._counter = max(self._counter - 1, 0)


class SqlAlchemyAsyncEngine(AsyncEngine[AsyncSession], SqlEngine):
    def __init__(self, backend: SqlEngineBackend, name: str, engine, metadata,
                 db_type: SqlEngineType, session_factory, timeout: timedelta):
        AsyncEngine.__init__(self, backend)
        SqlEngine.__init__(self, name, engine, metadata, db_type, timeout)

        self._session_factory = async_scoped_session(
            session_factory, scopefunc=lambda: get_context().session_id
        )
        self._lock = asyncio.Lock()
        self._counter = 0

    @property
    def connection_class(self):
        return AsyncSession

    @asynccontextmanager
    async def session(self, begin_tx: bool = True, force_rollback: bool = False) \
            -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        if self._session_factory.registry.has():
            yield self._session_factory()
            return

        session: AsyncSession = self._session_factory()

        if begin_tx:
            async with session.begin() as tx:
                yield session

                if sys.exc_info()[0] or force_rollback:
                    await tx.rollback()
                else:
                    await tx.commit()
        else:
            yield session

    async def teardown_session(self):
        await self._session_factory.remove()

    async def start(self):
        async with self._lock:
            if 0 == self._counter:
                logger.info(tr('dropland.engines.sql.engine.started')
                            .format(name=self.name, db_type=self.db_type, async_=f'async=True'))
            self._counter += 1

    async def stop(self):
        async with self._lock:
            if 1 == self._counter:
                await self.raw_engine.dispose()
                logger.info(tr('dropland.engines.sql.engine.stopped')
                            .format(name=self.name, db_type=self.db_type, async_=f'async=True'))
            self._counter = max(self._counter - 1, 0)
