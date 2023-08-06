from abc import ABC, abstractmethod
from contextlib import contextmanager, asynccontextmanager, AbstractContextManager, AbstractAsyncContextManager
from typing import Optional, Union, List, Mapping, Callable, TypeVar, Generic

SessionType = TypeVar('SessionType')


class EngineBackend(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def create_engine(self, name: str, *args, **kwargs) -> Union['SyncEngine', 'AsyncEngine']:
        ...

    @abstractmethod
    def get_engine(self, name: str) -> Optional[Union['SyncEngine', 'AsyncEngine']]:
        ...

    @abstractmethod
    def get_engine_names(self) -> List[str]:
        ...

    @abstractmethod
    def get_engines(self, names: Optional[List[str]] = None) -> Mapping[str, Union['SyncEngine', 'AsyncEngine']]:
        ...


class SyncEngine(Generic[SessionType], ABC):
    is_sync = True
    is_async = False

    def __init__(self, backend: EngineBackend):
        self._backend = backend

    @property
    def backend(self):
        return self._backend

    @contextmanager
    @abstractmethod
    def session(self, *args, **kwargs) -> Callable[..., AbstractContextManager[SessionType]]:
        ...

    def teardown_session(self):
        pass

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class AsyncEngine(Generic[SessionType], ABC):
    is_sync = False
    is_async = True

    def __init__(self, backend: EngineBackend):
        self._backend = backend

    @property
    def backend(self):
        return self._backend

    @asynccontextmanager
    @abstractmethod
    async def session(self, *args, **kwargs) -> Callable[..., AbstractAsyncContextManager[SessionType]]:
        ...

    async def teardown_session(self):
        pass

    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def stop(self):
        ...
