from dropland.engines.sqla import USE_SQLA

if USE_SQLA:
    from tests.conftest import sql_storage

    sqla_sqlite = sql_storage.create_engine('asqlite')
    sqla_pg = sql_storage.create_engine('apg')
    sqla_mysql = sql_storage.create_engine('ams')
