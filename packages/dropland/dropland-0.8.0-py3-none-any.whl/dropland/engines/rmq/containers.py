from dependency_injector import containers, providers

from dropland.app.base import ContainerResource, SessionResource
from dropland.util import default_value
from .engine import EngineConfig, RmqEngineBackend


class RmqResource(ContainerResource, SessionResource):
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

    async def session_begin(self, *args, **kwargs):
        pass

    async def session_finish(self, *args, **kwargs):
        for engine in reversed(self.container.engine_factory().get_engines().values()):
            if engine.is_async:
                await engine.teardown_session()
            else:
                engine.teardown_session()

    def get_engine(self, *args, **kwargs):
        if isinstance(self.container, SingleRmqContainer) or 'SingleRmqContainer' == self.container.parent_name:
            return self.container.create_engine()
        return self.container.create_engine(*args, **kwargs)


class RmqContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()
    engine_factory = providers.Singleton(RmqEngineBackend)

    def _create_engine(self, *args, **kwargs):
        return self.engine_factory().create_engine(*args, **kwargs)

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(RmqResource, __self__)


class SingleRmqContainer(RmqContainer):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self):
        if isinstance(self.config.engine_config(), EngineConfig):
            engine_config = self.config.engine_config()
        else:
            engine_config = EngineConfig(
                url=self.config.engine_config.url(),
                virtualhost=self.config.engine_config.virtualhost(),
                timeout_seconds=self.config.engine_config.
                    timeout_seconds.as_(default_value(int))(default=5),
                pool_max_connections=self.config.engine_config.
                    pool_max_connections.as_(default_value(int))(default=4),
                pool_max_channels_per_connection=self.config.engine_config.
                    pool_max_channels_per_connection.as_(default_value(int))(default=100)
            )
        return RmqContainer._create_engine(self, self.config.name(), engine_config)

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(RmqResource, __self__)


class MultipleRmqContainer(RmqContainer):
    __self__ = providers.Self()
    config = providers.Configuration()

    def _create_engine(self, name: str):
        if conf := self.config.get(name):
            if isinstance(conf['engine_config'], EngineConfig):
                engine_config = conf['engine_config']
            else:
                engine_config = EngineConfig(
                    url=conf['engine_config']['url'],
                    virtualhost=conf['engine_config']['virtualhost'],
                    timeout_seconds=int(conf['engine_config'].get('timeout_seconds', 5)),
                    pool_max_connections=int(conf['engine_config'].get('pool_max_connections', 4)),
                    pool_max_channels_per_connection=int(conf['engine_config'].get(
                        'pool_max_channels_per_connection', 100))
                )
            return RmqContainer._create_engine(self, name, engine_config)
        return None

    create_engine = providers.Factory(_create_engine, __self__)
    instance = providers.Singleton(RmqResource, __self__)
