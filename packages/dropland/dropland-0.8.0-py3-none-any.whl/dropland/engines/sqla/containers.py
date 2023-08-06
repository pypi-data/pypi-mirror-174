from dependency_injector import containers, providers

from dropland.app.base import ContainerResource, SessionResource
from dropland.util import default_value
from .engine import EngineConfig, SqlEngineBackend


class SqlaResource(ContainerResource, SessionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sync_initialized = self._async_initialized = False
        self._sync_sessions = list()
        self._async_sessions = list()

    def sync_startup(self, *args, **kwargs):
        if self._sync_initialized:
            return

        for engine in self.container.engine_factory().get_engines().values():
            if not engine.is_async:
                engine.start()

        self._sync_initialized = True

    def sync_shutdown(self, *args, **kwargs):
        if not self._sync_initialized:
            return

        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if not engine.is_async:
                engine.stop()

        self._sync_initialized = False

    async def startup(self, *args, **kwargs):
        if self._async_initialized:
            return

        for engine in self.container.engine_factory().get_engines().values():
            if engine.is_async:
                await engine.start()

        self._async_initialized = True

    async def shutdown(self, *args, **kwargs):
        if not self._async_initialized:
            return

        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if engine.is_async:
                await engine.stop()

        self._async_initialized = False

    def sync_session_begin(self, begin_tx: bool = True, force_rollback: bool = False, *args, **kwargs):
        if not self._sync_initialized:
            return

        for engine in self.container.engine_factory().get_engines().values():
            if not engine.is_async:
                session = engine.session(begin_tx=begin_tx, force_rollback=force_rollback)
                session.__aenter__()
                self._sync_sessions.append(session)

    def sync_session_finish(self, *args, **kwargs):
        if not self._sync_initialized:
            return

        for session in reversed(self._sync_sessions):
            session.__exit__(None, None, None)
        self._sync_sessions.clear()

        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if not engine.is_async:
                engine.teardown_session()

    async def session_begin(self, begin_tx: bool = True, force_rollback: bool = False, *args, **kwargs):
        if not self._async_initialized:
            return

        for engine in self.container.engine_factory().get_engines().values():
            if engine.is_async:
                session = engine.session(begin_tx=begin_tx, force_rollback=force_rollback)
                await session.__aenter__()
                self._async_sessions.append(session)

    async def session_finish(self, *args, **kwargs):
        if not self._async_initialized:
            return

        for session in reversed(self._async_sessions):
            await session.__aexit__(None, None, None)
        self._async_sessions.clear()

        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if engine.is_async:
                await engine.teardown_session()

    def get_engine(self, *args, **kwargs):
        if isinstance(self.container, SingleSqlaContainer) or 'SingleSqlContainer' == self.container.parent_name:
            return self.container.create_engine()
        return self.container.create_engine(*args, **kwargs)


class SqlaContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()
    engine_factory = providers.Singleton(SqlEngineBackend)

    def _create_engine(self, *args, **kwargs):
        return self.engine_factory().create_engine(*args, **kwargs)

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(SqlaResource, __self__)


class SingleSqlaContainer(SqlaContainer):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self):
        if isinstance(self.config.engine_config(), EngineConfig):
            engine_config = self.config.engine_config()
        else:
            engine_config = EngineConfig(
                url=self.config.engine_config.url(),
                echo=self.config.engine_config.echo.as_(bool)(),
                pool_min_size=self.config.engine_config.
                    pool_min_size.as_(default_value(int))(default=1),
                pool_max_size=self.config.engine_config.
                    pool_max_size.as_(default_value(int))(default=8),
                pool_expire_seconds=self.config.engine_config.
                    pool_expire_seconds.as_(default_value(int))(default=60),
                pool_timeout_seconds=self.config.engine_config.
                    pool_timeout_seconds.as_(default_value(int))(default=15)
            )
        return SqlaContainer._create_engine(
            self, self.config.name(), engine_config, self.config.db_type(),
            use_async=self.config.use_async.as_(bool)()
        )

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(SqlaResource, __self__)


class MultipleSqlaContainer(SqlaContainer):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self, name: str):
        if conf := self.config.get(name):
            if isinstance(conf['engine_config'], EngineConfig):
                engine_config = conf['engine_config']
            else:
                engine_config = EngineConfig(
                    url=conf['engine_config']['url'],
                    echo=bool(conf['engine_config'].get('echo')),
                    pool_min_size=int(conf['engine_config'].get('pool_min_size', 1)),
                    pool_max_size=int(conf['engine_config'].get('pool_max_size', 8)),
                    pool_expire_seconds=int(conf['engine_config'].get('pool_expire_seconds', 60)),
                    pool_timeout_seconds=int(conf['engine_config'].get('pool_timeout_seconds', 15))
                )
            return SqlaContainer._create_engine(
                self, name, engine_config, conf['db_type'], use_async=conf.get('use_async', False)
            )
        return None

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(SqlaResource, __self__)
