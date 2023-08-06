from dependency_injector import containers, providers

from dropland.app.base import ContainerResource, SessionResource
from dropland.util import default_value
from .engine import EngineConfig, DbEngineBackend


class DbResource(ContainerResource, SessionResource):
    async def startup(self, *args, **kwargs):
        if self.initialized:
            return

        for engine in self.container.engine_factory().get_engines().values():
            if engine.is_async:
                await engine.start()
            else:
                engine.start()

        self._initialized = True

    async def shutdown(self, *args, **kwargs):
        if not self.initialized:
            return

        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if engine.is_async:
                await engine.stop()
            else:
                engine.stop()

        self._initialized = False

    async def session_begin(self, begin_tx: bool = True, force_rollback: bool = False, *args, **kwargs):
        pass

    async def session_finish(self, *args, **kwargs):
        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if engine.is_async:
                await engine.teardown_session()
            else:
                engine.teardown_session()

    def get_engine(self, *args, **kwargs):
        if isinstance(self.container, SingleDbContainer) or 'SingleDbContainer' == self.container.parent_name:
            return self.container.create_engine()
        return self.container.create_engine(*args, **kwargs)


class DbContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()
    engine_factory = providers.Singleton(DbEngineBackend)

    def _create_engine(self, *args, **kwargs):
        return self.engine_factory().create_engine(*args, **kwargs)

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(DbResource, __self__)


class SingleDbContainer(DbContainer):
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
            )
        return DbContainer._create_engine(
            self, self.config.name(), engine_config, self.config.db_type()
        )

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(DbResource, __self__)


class MultipleDbContainer(DbContainer):
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
                )
            return DbContainer._create_engine(self, name, engine_config, conf['db_type'])
        return None

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(DbResource, __self__)
