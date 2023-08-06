import pytest

from dropland.engines.databases import USE_DB

pytestmark = pytest.mark.skipif(not USE_DB, reason='For Databases only')

if USE_DB:
    from dropland.engines.sql import SqlEngineType
    from dropland.engines.databases.containers import DbContainer, SingleDbContainer, MultipleDbContainer
    from dropland.engines.databases import EngineConfig, DbEngine
    from tests import MYSQL_URI, POSTGRES_URI, SQLITE_URI


@pytest.mark.asyncio
async def test_create_engine():
    sqlite_config = EngineConfig(
        url=SQLITE_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )
    pg_config = EngineConfig(
        url=POSTGRES_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )
    mysql_config = EngineConfig(
        url=MYSQL_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )

    default_db_storage = DbContainer()
    engine_factory = default_db_storage.engine_factory()

    assert not engine_factory.get_engine('')

    assert engine_factory.create_engine('sqlite', sqlite_config, SqlEngineType.SQLITE)
    assert engine_factory.create_engine('pg', pg_config, SqlEngineType.POSTGRES)
    assert engine_factory.create_engine('ms', mysql_config, SqlEngineType.MYSQL)

    for db_type in (SqlEngineType.SQLITE, SqlEngineType.POSTGRES, SqlEngineType.MYSQL):
        for e in engine_factory.get_engines_for_type(db_type):
            assert e.db_type == db_type
            assert e.is_async

    assert engine_factory.get_engine_names() == ['sqlite', 'pg', 'ms']


@pytest.mark.asyncio
async def test_sqlite_engine():
    sqlite_config = EngineConfig(
        url=SQLITE_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )

    default_db_storage = DbContainer()
    engine_factory = default_db_storage.engine_factory()
    sqlite_engine = engine_factory.create_engine('sqlite', sqlite_config, SqlEngineType.SQLITE)

    await sqlite_engine.start()

    async with sqlite_engine.session() as conn:
        res = await conn.fetch_val('select sqlite_version();')
        print(res)
        res = await conn.fetch_val('select 1 + 2;')
        assert res == 3

    await sqlite_engine.stop()


@pytest.mark.asyncio
async def test_pg_engine():
    pg_config = EngineConfig(
        url=POSTGRES_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )

    default_db_storage = DbContainer()
    engine_factory = default_db_storage.engine_factory()
    pg_engine = engine_factory.create_engine('pg', pg_config, SqlEngineType.POSTGRES)

    await pg_engine.start()

    async with pg_engine.session() as conn:
        res = await conn.fetch_val('select version();')
        print(res)
        res = await conn.fetch_val('select 1 + 2;')
        assert res == 3

    await pg_engine.stop()


@pytest.mark.asyncio
async def test_mysql_engine():
    mysql_config = EngineConfig(
        url=MYSQL_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )

    default_db_storage = DbContainer()
    engine_factory = default_db_storage.engine_factory()
    mysql_engine = engine_factory.create_engine('ms', mysql_config, SqlEngineType.MYSQL)

    await mysql_engine.start()

    async with mysql_engine.session() as conn:
        res = await conn.fetch_val('select version();')
        print(res)
        res = await conn.fetch_val('select 1 + 2;')
        assert res == 3

    await mysql_engine.stop()


@pytest.mark.asyncio
async def test_storage_container():
    sqlite_config = EngineConfig(
        url=SQLITE_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )
    pg_config = EngineConfig(
        url=POSTGRES_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )
    mysql_config = EngineConfig(
        url=MYSQL_URI,
        pool_min_size=1, pool_max_size=2,
        pool_expire_seconds=15,
    )

    cont = DbContainer()

    eng = cont.create_engine('dropland', sqlite_config, SqlEngineType.SQLITE)
    assert isinstance(eng, DbEngine)
    assert eng.name == 'dropland'
    cont.unwire()

    cont = SingleDbContainer()
    cont.config.from_dict({
        'name': '_',
        'db_type': SqlEngineType.SQLITE,
        'engine_config': sqlite_config,
    })
    eng1 = cont.create_engine()
    eng2 = cont.create_engine()
    assert eng1.name == eng2.name == '_'
    assert eng1 is eng2
    cont.unwire()

    cont = MultipleDbContainer()
    cont.config.from_dict({
        'one': {
            'db_type': SqlEngineType.SQLITE,
            'engine_config': sqlite_config,
        },
        'two': {
            'db_type': SqlEngineType.POSTGRES,
            'engine_config': pg_config,
        },
        'three': {
            'db_type': SqlEngineType.MYSQL,
            'engine_config': mysql_config,
        },
    })

    eng1 = cont.create_engine('one')
    eng2 = cont.create_engine('two')
    eng3 = cont.create_engine('three')
    assert eng1 is not eng2 is not eng3
    assert eng1.is_async is True
    assert eng2.is_async is True
    assert eng3.is_async is True
    assert eng1.name == 'one'
    assert eng2.name == 'two'
    assert eng3.name == 'three'

    cont.unwire()
