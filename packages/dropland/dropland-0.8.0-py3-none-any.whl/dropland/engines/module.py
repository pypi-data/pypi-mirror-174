from dependency_injector import containers, providers

from app.module import Module
from .databases import USE_DB
from .redis import USE_REDIS
from .rmq import USE_RMQ
from .scheduler import USE_SCHEDULER
from .sqla import USE_SQLA

__engines__ = dict()


if USE_DB:
    from .databases.containers import DbResource
    __engines__['db'] = DbResource

if USE_REDIS:
    from .redis.containers import RedisResource
    __engines__['redis'] = RedisResource

if USE_RMQ:
    from .rmq.containers import RmqResource
    __engines__['rmq'] = RmqResource

if USE_SCHEDULER:
    from .scheduler.containers import SchedulerResource
    __engines__['scheduler'] = SchedulerResource

if USE_SQLA:
    from .sqla.containers import SqlaResource
    __engines__['sql'] = SqlaResource


class EnginesContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()

    engines = providers.Aggregate(**{
        name: providers.Factory(class_) for name, class_ in __engines__.items()
    })


class EnginesModule(Module):
    pass

