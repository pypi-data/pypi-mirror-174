import pytest

from tests.sql_models_data import USE_SQLA

pytestmark = pytest.mark.skipif(not USE_SQLA, reason='For SqlAlchemy only')

if USE_SQLA:
    from dropland.engines.sql import SqlEngineType
    from dropland.engines.sqla.containers import SqlaContainer, SingleSqlaContainer, MultipleSqlaContainer
    from dropland.engines.sqla import EngineConfig, SqlEngine
    from tests import MYSQL_URI, POSTGRES_URI, SQLITE_URI


@pytest.mark.asyncio
async def test_create_engine():
    sqlite_config = EngineConfig(
        url=SQLITE_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15, pool_timeout_seconds=15,
    )
    pg_config = EngineConfig(
        url=POSTGRES_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15, pool_timeout_seconds=15,
    )
    mysql_config = EngineConfig(
        url=MYSQL_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15, pool_timeout_seconds=15,
    )

    default_sql_storage = SqlaContainer()
    engine_factory = default_sql_storage.engine_factory()

    assert engine_factory.create_engine('sqlite', sqlite_config, SqlEngineType.SQLITE, use_async=False)
    assert engine_factory.create_engine('asqlite', sqlite_config, SqlEngineType.SQLITE, use_async=True)
    assert engine_factory.create_engine('pg', pg_config, SqlEngineType.POSTGRES, use_async=False)
    assert engine_factory.create_engine('apg', pg_config, SqlEngineType.POSTGRES, use_async=True)
    assert engine_factory.create_engine('ms', mysql_config, SqlEngineType.MYSQL, use_async=False)
    assert engine_factory.create_engine('ams', mysql_config, SqlEngineType.MYSQL, use_async=True)

    for db_type in (SqlEngineType.SQLITE, SqlEngineType.POSTGRES, SqlEngineType.MYSQL):
        for e in engine_factory.get_engines_for_type(db_type, is_async=False):
            assert e.db_type == db_type
            assert not e.is_async

        for e in engine_factory.get_engines_for_type(db_type, is_async=True):
            assert e.db_type == db_type
            assert e.is_async

    assert engine_factory.get_engine_names() == ['sqlite', 'asqlite', 'pg', 'apg', 'ms', 'ams']


def test_sqlite_engine(sqlite_engine):
    sqlite_engine.start()

    with sqlite_engine.session() as conn:
        res = conn.execute('select sqlite_version();')
        print(res.fetchone()[0])
        res = conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    sqlite_engine.stop()


@pytest.mark.asyncio
async def test_async_sqlite_engine(sqlite_async_engine):
    await sqlite_async_engine.start()

    async with sqlite_async_engine.session() as conn:
        res = await conn.execute('select sqlite_version();')
        print(res.fetchone()[0])
        res = await conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    await sqlite_async_engine.stop()


def test_pg_engine(pg_engine):
    pg_engine.start()

    with pg_engine.session() as conn:
        res = conn.execute('select version();')
        print(res.fetchone()[0])
        res = conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    pg_engine.stop()


@pytest.mark.asyncio
async def test_async_pg_engine(pg_async_engine):
    await pg_async_engine.start()

    async with pg_async_engine.session() as conn:
        res = await conn.execute('select version();')
        print(res.fetchone()[0])
        res = await conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    await pg_async_engine.stop()


def test_mysql_engine(mysql_engine):
    mysql_engine.start()

    with mysql_engine.session() as conn:
        res = conn.execute('select version();')
        print(res.fetchone()[0])
        res = conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    mysql_engine.stop()


@pytest.mark.asyncio
async def test_async_mysql_engine(mysql_async_engine):
    await mysql_async_engine.start()

    async with mysql_async_engine.session() as conn:
        res = await conn.execute('select version();')
        print(res.fetchone()[0])
        res = await conn.execute('select 1 + 2;')
        assert res.fetchone()[0] == 3

    await mysql_async_engine.stop()


@pytest.mark.asyncio
async def test_storage_container():
    sqlite_config = EngineConfig(
        url=SQLITE_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15, pool_timeout_seconds=15,
    )

    cont = SqlaContainer()

    eng = cont.create_engine('dropland', sqlite_config, SqlEngineType.SQLITE, use_async=False)
    assert isinstance(eng, SqlEngine)
    assert eng.name == 'dropland'
    cont.unwire()

    cont = SingleSqlaContainer()
    cont.config.from_dict({
        'name': '_',
        'db_type': SqlEngineType.SQLITE,
        'engine_config': sqlite_config,
        'use_async': False,
    })
    eng1 = cont.create_engine()
    eng2 = cont.create_engine()
    assert eng1.name == eng2.name == '_'
    assert eng1 is eng2
    cont.unwire()

    cont = MultipleSqlaContainer()
    cont.config.from_dict({
        'one': {
            'db_type': SqlEngineType.SQLITE,
            'engine_config': sqlite_config,
            'use_async': False,
        },
        'two': {
            'db_type': SqlEngineType.SQLITE,
            'engine_config': sqlite_config,
            'use_async': True,
        },
    })

    eng1 = cont.create_engine('one')
    eng2 = cont.create_engine('two')
    assert eng1 is not eng2
    assert eng1.is_async is False
    assert eng2.is_async is True
    assert eng1.name == 'one'
    assert eng2.name == 'two'

    cont.unwire()
