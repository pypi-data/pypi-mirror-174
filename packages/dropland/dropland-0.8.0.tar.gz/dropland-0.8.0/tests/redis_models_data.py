from dropland.engines.redis import USE_REDIS

if USE_REDIS:
    from dropland.engines.redis.containers import RedisContainer
    from dropland.engines.redis.engine import EngineConfig

from tests import REDIS_URI

if USE_REDIS:
    redis_container = RedisContainer()
    redis_engine = redis_container.create_engine('dropland', EngineConfig(url=REDIS_URI))
