import asyncio

import pytest

from dropland.engines.redis import USE_REDIS
from dropland.engines.rmq import USE_RMQ
from dropland.engines.sql import SqlEngineType
from dropland.engines.sqla import USE_SQLA

if USE_REDIS:
    from dropland.engines.redis.containers import RedisResource
    from dropland.engines.redis.engine import EngineConfig as RedisEngineConfig
    from .redis_models_data import redis_container

if USE_RMQ:
    from dropland.engines.rmq.containers import RmqContainer, RmqResource
    from dropland.engines.rmq.engine import EngineConfig as RmqEngineConfig

if USE_SQLA:
    from dropland.engines.sqla.containers import MultipleSqlaContainer, SqlaContainer, SqlaResource
    from dropland.engines.sqla import EngineConfig as SqlEngineConfig

from tests import MYSQL_URI, POSTGRES_URI, REDIS_URI, RMQ_URI, SQLITE_URI


if USE_SQLA:
    sql_storage = MultipleSqlaContainer()

    sql_storage.config.from_dict({
        'sqlite': {
            'db_type': SqlEngineType.SQLITE,
            'engine_config': SqlEngineConfig(
                url=SQLITE_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': False
        },
        'asqlite': {
            'db_type': SqlEngineType.SQLITE,
            'engine_config': SqlEngineConfig(
                url=SQLITE_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': True
        },
        'pg': {
            'db_type': SqlEngineType.POSTGRES,
            'engine_config': SqlEngineConfig(
                url=POSTGRES_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': False
        },
        'apg': {
            'db_type': SqlEngineType.POSTGRES,
            'engine_config': SqlEngineConfig(
                url=POSTGRES_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': True
        },
        'ms': {
            'db_type': SqlEngineType.MYSQL,
            'engine_config': SqlEngineConfig(
                url=MYSQL_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': False
        },
        'ams': {
            'db_type': SqlEngineType.MYSQL,
            'engine_config': SqlEngineConfig(
                url=MYSQL_URI,
                pool_min_size=1, pool_max_size=2,
                pool_expire_seconds=15, pool_timeout_seconds=15,
            ),
            'use_async': True
        },
    })


@pytest.fixture(scope='session')
def test_sql_storage():
    if USE_SQLA:
        return SqlaContainer()
    else:
        return None


@pytest.fixture(scope='session')
def test_redis_storage():
    if USE_REDIS:
        return redis_container
    else:
        return None


@pytest.fixture(scope='session')
def test_rmq_storage():
    if USE_RMQ:
        return RmqContainer()
    else:
        return None


@pytest.fixture(scope='session')
def sql_sync_engine(test_sql_storage):
    conf = sql_storage.config.get('sqlite')
    return test_sql_storage.create_engine(
        'dropland-test-sync', conf['engine_config'], conf['db_type'], conf.get('use_async')
    )


@pytest.fixture(scope='session')
def sql_async_engine(test_sql_storage):
    conf = sql_storage.config.get('asqlite')
    return test_sql_storage.create_engine(
        'dropland-test-async', conf['engine_config'], conf['db_type'], conf.get('use_async')
    )


@pytest.fixture(scope='session')
def sqlite_engine():
    return sql_storage.create_engine('sqlite')


@pytest.fixture(scope='session')
def sqlite_async_engine():
    return sql_storage.create_engine('asqlite')


@pytest.fixture(scope='session')
def pg_engine():
    return sql_storage.create_engine('pg')


@pytest.fixture(scope='session')
def pg_async_engine():
    return sql_storage.create_engine('apg')


@pytest.fixture(scope='session')
def mysql_engine():
    return sql_storage.create_engine('ms')


@pytest.fixture(scope='session')
def mysql_async_engine():
    return sql_storage.create_engine('ams')


@pytest.fixture(scope='session')
def redis_engine(test_redis_storage):
    engine_config = RedisEngineConfig(url=REDIS_URI)
    return test_redis_storage.create_engine('dropland', engine_config)


@pytest.fixture(scope='session')
def rmq_engine(test_rmq_storage):
    engine_config = RmqEngineConfig(url=RMQ_URI)
    return test_rmq_storage.create_engine('dropland', engine_config)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


if USE_SQLA:
    @pytest.fixture(scope='function')
    def sync_sql_session(event_loop, test_sql_storage):
        resource = SqlaResource(test_sql_storage)
        resource.sync_startup()
        resource.sync_session_begin(force_rollback=True)
        yield
        resource.sync_session_finish()
        resource.sync_shutdown()

    @pytest.fixture(scope='function')
    async def async_sql_session(event_loop, test_sql_storage):
        resource = SqlaResource(test_sql_storage)
        await resource.startup()
        await resource.session_begin(force_rollback=True)
        yield
        await resource.session_finish()
        await resource.shutdown()


if USE_REDIS:
    @pytest.fixture(scope='module')
    def wire_redis_storage(test_redis_storage):
        test_redis_storage.wire()
        yield
        test_redis_storage.unwire()

    @pytest.fixture(scope='function')
    async def redis_session(event_loop, wire_redis_storage, test_redis_storage, redis_engine):
        resource = RedisResource(test_redis_storage)
        await resource.startup()
        await resource.session_begin()
        yield
        await resource.session_finish()
        await resource.shutdown()


if USE_RMQ:
    @pytest.fixture(scope='module')
    def wire_rmq_storage(test_rmq_storage):
        test_rmq_storage.wire()
        yield
        test_rmq_storage.unwire()

    @pytest.fixture(scope='function')
    async def rmq_session(event_loop, wire_rmq_storage, test_rmq_storage, rmq_engine):
        resource = RmqResource(test_rmq_storage)
        await resource.startup()
        await resource.session_begin()
        yield
        await resource.session_finish()
        await resource.shutdown()
