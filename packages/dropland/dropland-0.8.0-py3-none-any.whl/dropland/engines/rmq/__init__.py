try:
    import aio_pika

    from .engine import EngineConfig, RmqEngineBackend, RmqEngine
    from .settings import RmqSettings

    USE_RMQ = True

except ImportError:
    USE_RMQ = False
