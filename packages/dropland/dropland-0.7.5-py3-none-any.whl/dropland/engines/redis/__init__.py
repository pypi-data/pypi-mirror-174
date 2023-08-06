try:
    import aioredis

    from .engine import EngineConfig, RedisEngineBackend, RedisEngine
    from .model import RedisModel, RedisMethodCache
    from .settings import RedisSettings

    USE_REDIS = True

except ImportError:
    USE_REDIS = False
