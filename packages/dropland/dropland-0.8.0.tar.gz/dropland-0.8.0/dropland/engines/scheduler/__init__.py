try:
    import apscheduler

    from .engine import EngineConfig, SchedulerBackend
    from .local import Scheduler
    from .application import SchedulerApplication, SchedulerResource, SchedulerRPC
    from .settings import SchedulerSettings

    USE_SCHEDULER = True

except ImportError:
    USE_SCHEDULER = False
