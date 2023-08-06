from collections import defaultdict
from typing import Dict, List

from dropland.core.loaders.backend import BackendLoader
from dropland.engines.sql.base import SqlEngineType
from .engine import SqlEngineBackend


class SqlBackendLoader(BackendLoader[SqlEngineBackend]):
    def __init__(self):
        super().__init__('dropland.engines.sql', 'create_sql_storage_backend')
        self._db_support_dict: Dict[SqlEngineType, List[str]] = defaultdict(list)

    def on_load(self, backend: SqlEngineBackend):
        for db_type in backend.db_supports:
            self._db_support_dict[db_type].append(backend.name)

    def get_backends_for_db(self, db_type: SqlEngineType) -> List[str]:
        return self._db_support_dict.get(db_type, [])
