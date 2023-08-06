from typing import Dict, List, Optional

from dependency_injector.containers import Container

from . import base


class Module(base.Module, base.ContainerResource):
    def __init__(self, container: Container, name: str):
        super().__init__(container)

        self._name = name
        self._resource_containers: Dict[str, Container] = dict()
        self._resources: Dict[str, base.Resource] = dict()

        if hasattr(container, 'resources'):
            for name, provider in container.resources.providers.items():
                res_container = container.resources(name)
                self._resource_containers[name] = res_container
                self._resources[name] = res_container.instance(res_container)

    @property
    def name(self) -> str:
        return self._name

    @property
    def resources(self) -> List[base.Resource]:
        return list(self._resources.values())

    def get_resource(self, name) -> Optional[base.Resource]:
        return self._resources.get(name)

    def sync_startup(self, application=None, service=None, *args, **kwargs):
        for r in self.resources:
            r.sync_startup(application=application, service=service, module=self, *args, **kwargs)

    def sync_shutdown(self, application=None, service=None, *args, **kwargs):
        for r in self.resources:
            r.sync_shutdown(application=application, service=service, module=self, *args, **kwargs)

    async def startup(self, application=None, service=None, *args, **kwargs):
        for r in self.resources:
            await r.startup(application=application, service=service, module=self, *args, **kwargs)

    async def shutdown(self, application=None, service=None, *args, **kwargs):
        for r in self.resources:
            await r.shutdown(application=application, service=service, module=self, *args, **kwargs)


class SessionModule(Module, base.SessionResource):
    def sync_session_begin(self, application=None, service=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_begin(application=application, service=service, module=self, *args, **kwargs)

    def sync_session_finish(self, application=None, service=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_finish(application=application, service=service, module=self, *args, **kwargs)

    async def session_begin(self, application=None, service=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_begin(application=application, service=service, module=self, *args, **kwargs)

    async def session_finish(self, application=None, service=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_finish(application=application, service=service, module=self, *args, **kwargs)
