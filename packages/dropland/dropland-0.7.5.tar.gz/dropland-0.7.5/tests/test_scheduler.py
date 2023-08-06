import asyncio
import random
import time
from multiprocessing import Array, Process, Value

import pytest
from dependency_injector import containers, providers

from dropland.engines.redis import USE_REDIS
from dropland.engines.scheduler import USE_SCHEDULER
from tests import REDIS_URI, SQLITE_URI

pytestmark = pytest.mark.skipif(not USE_SCHEDULER, reason='For scheduler only')

if USE_SCHEDULER:
    from dropland.engines.scheduler.application import SchedulerApplication
    from dropland.engines.scheduler.containers import SimpleSchedulerContainer, SchedulerContainer
    from dropland.engines.scheduler.engine import EngineConfig
    default_scheduler_module = SimpleSchedulerContainer()


def test_create_engine():
    engine_factory = default_scheduler_module.engine_factory()

    assert not engine_factory.get_engine('')

    if USE_REDIS:
        config = EngineConfig(sql_url=SQLITE_URI, redis_url=REDIS_URI)
    else:
        config = EngineConfig(sql_url=SQLITE_URI)

    assert not engine_factory.get_engine('dropland')
    assert engine_factory.create_engine('dropland', config)
    assert engine_factory.get_engine('dropland')

    assert engine_factory.get_engine_names() == ['dropland']

    assert engine_factory.create_engine('dropland-remote', config)
    assert engine_factory.get_engine('dropland')
    assert engine_factory.get_engine('dropland-remote')

    assert engine_factory.get_engine_names() == ['dropland', 'dropland-remote']


job_called = 0
job_call_args = []
process_job_called = Value('i', 0)
process_job_call_args = Array('i', 2)
SLEEP_DURATION = 0.01


def task_fn(a):
    global job_called, job_call_args
    job_called += 1
    job_call_args.append(a)


async def async_task_fn(a):
    global job_called, job_call_args
    job_called += 1
    job_call_args.append(a)


def process_task_fn(a):
    global process_job_called, process_job_call_args
    process_job_call_args[process_job_called.value] = a
    process_job_called.value += 1
    time.sleep(SLEEP_DURATION)


async def async_process_task_fn(a):
    global process_job_called, process_job_call_args
    process_job_call_args[process_job_called.value] = a
    process_job_called.value += 1
    await asyncio.sleep(SLEEP_DURATION)


_current_app = None


def create_scheduler_app(with_remote: bool = False):
    settings = {
        'name': str(random.randint(0, 1000)),
        'engine_config': {
            'sql_url': SQLITE_URI,
            'create_remote_engine': with_remote,
            'task_host': 'localhost',
            'task_port': 3000,
        }
    }

    if USE_REDIS:
        settings['engine_config']['redis_url'] = REDIS_URI

    app_container = containers.DynamicContainer()
    app_container.blocks = providers.Aggregate(
        scheduler=providers.Factory(SchedulerContainer, config=settings)
    )

    app = SchedulerApplication(app_container, settings['name'], settings['engine_config'])
    app.path = 'tests.test_scheduler:_current_app'
    app_container.instance = providers.Object(app)

    global _current_app
    _current_app = app
    return app


@pytest.fixture(scope='function')
def scheduler_app():
    return create_scheduler_app()


@pytest.fixture(scope='function')
def remote_scheduler_app():
    return create_scheduler_app(True)


@pytest.mark.parametrize('target', (task_fn, async_task_fn), ids=['SyncTarget', 'AsyncTarget'])
def test_sync_run_tasks_as_local(target, scheduler_app):
    global job_called, job_call_args
    job_called, job_call_args = 0, []

    scheduler = scheduler_app.scheduler
    scheduler.start()
    scheduler.add_job(target, args=['123'], trigger='date')

    while job_called == 0:
        time.sleep(SLEEP_DURATION)

    scheduler.add_job(target, args=['456'], trigger='date', jobstore='sql')

    while job_called == 1:
        time.sleep(SLEEP_DURATION)

    if USE_REDIS:
        scheduler.add_job(target, args=['789'], trigger='date', jobstore='redis')

        while job_called == 2:
            time.sleep(SLEEP_DURATION)

    scheduler.shutdown()

    if USE_REDIS:
        assert job_called == 3
        assert job_call_args == ['123', '456', '789']
    else:
        assert job_called == 2
        assert job_call_args == ['123', '456']


@pytest.mark.asyncio
@pytest.mark.parametrize('target', (task_fn, async_task_fn), ids=['SyncTarget', 'AsyncTarget'])
async def test_async_run_tasks_as_local(target, scheduler_app):
    global job_called, job_call_args
    job_called, job_call_args = 0, []

    scheduler = scheduler_app.scheduler
    scheduler.start()
    scheduler.add_job(target, args=['123'], trigger='date')

    while job_called == 0:
        await asyncio.sleep(SLEEP_DURATION)

    scheduler.add_job(target, args=['456'], trigger='date', jobstore='sql')

    while job_called == 1:
        await asyncio.sleep(SLEEP_DURATION)

    if USE_REDIS:
        scheduler.add_job(target, args=['789'], trigger='date', jobstore='redis')

        while job_called == 2:
            await asyncio.sleep(SLEEP_DURATION)

    scheduler.shutdown()

    if USE_REDIS:
        assert job_called == 3
        assert job_call_args == ['123', '456', '789']
    else:
        assert job_called == 2
        assert job_call_args == ['123', '456']


@pytest.mark.parametrize('target', (process_task_fn, async_process_task_fn), ids=['SyncTarget', 'AsyncTarget'])
def test_sync_run_tasks_as_interprocess(target, scheduler_app):
    global process_job_called, process_job_call_args
    process_job_called, process_job_call_args = Value('i', 0), Array('i', 2)

    scheduler = scheduler_app.scheduler
    scheduler.start()
    scheduler.add_job(target, args=[1], trigger='date', jobstore='sql', executor='process')

    while process_job_called.value == 0:
        time.sleep(SLEEP_DURATION)

    if USE_REDIS:
        scheduler.add_job(target, args=[2], trigger='date', jobstore='redis', executor='process')

        while process_job_called.value == 1:
            time.sleep(SLEEP_DURATION)

    scheduler.shutdown()

    if USE_REDIS:
        assert process_job_called.value == 2
        assert process_job_call_args[:] == [1, 2]
    else:
        assert process_job_called.value == 1
        assert process_job_call_args[:] == [1, 0]


@pytest.mark.asyncio
@pytest.mark.parametrize('target', (process_task_fn, async_process_task_fn), ids=['SyncTarget', 'AsyncTarget'])
async def test_async_run_tasks_as_interprocess(target, scheduler_app):
    global process_job_called, process_job_call_args
    process_job_called, process_job_call_args = Value('i', 0), Array('i', 2)

    scheduler = scheduler_app.scheduler
    scheduler.start()
    scheduler.add_job(target, args=[3], trigger='date', jobstore='sql', executor='process')

    while process_job_called.value == 0:
        await asyncio.sleep(SLEEP_DURATION)

    if USE_REDIS:
        scheduler.add_job(target, args=[4], trigger='date', jobstore='redis', executor='process')

        while process_job_called.value == 1:
            await asyncio.sleep(SLEEP_DURATION)

    scheduler.shutdown()

    if USE_REDIS:
        assert process_job_called.value == 2
        assert process_job_call_args[:] == [3, 4]
    else:
        assert process_job_called.value == 1
        assert process_job_call_args[:] == [3, 0]


@pytest.mark.parametrize('target', (process_task_fn, async_process_task_fn), ids=['SyncTarget', 'AsyncTarget'])
@pytest.mark.parametrize('executor', ('default', 'process'), ids=['Default', 'Process'])
def test_run_tasks_as_remote(target, executor: str, remote_scheduler_app):
    global process_job_called, process_job_call_args
    process_job_called, process_job_call_args = Value('i', 0), Array('i', 2)

    from dropland.engines.scheduler.application import run_service
    p = Process(target=run_service)
    p.start()
    time.sleep(SLEEP_DURATION * 10)

    remote_scheduler = remote_scheduler_app.scheduler
    remote_scheduler.start()
    remote_scheduler.add_job(target, args=[5], trigger='date', jobstore='sql', executor=executor)

    while process_job_called.value == 0:
        time.sleep(SLEEP_DURATION)

    if USE_REDIS:
        remote_scheduler.add_job(target, args=[6], trigger='date', jobstore='redis', executor=executor)

        while process_job_called.value == 1:
            time.sleep(SLEEP_DURATION)

    remote_scheduler.shutdown()
    time.sleep(SLEEP_DURATION * 10)
    p.terminate()
    p.join()

    if USE_REDIS:
        assert process_job_called.value == 2
        assert process_job_call_args[:] == [5, 6]
    else:
        assert process_job_called.value == 1
        assert process_job_call_args[:] == [5, 0]


@pytest.mark.parametrize('target', (process_task_fn, async_process_task_fn), ids=['SyncTarget', 'AsyncTarget'])
@pytest.mark.parametrize('executor', ('default', 'process'), ids=['Default', 'Process'])
@pytest.mark.parametrize('remote', (False, True), ids=['Local', 'Remote'])
def test_scheduled_job(target, executor: str, remote: bool):
    global process_job_called, process_job_call_args
    process_job_called, process_job_call_args = Value('i', 0), Array('i', 2)

    if remote:
        from dropland.engines.scheduler.application import run_service
        p = Process(target=run_service)
        p.start()

    scheduler_app = create_scheduler_app(remote)
    scheduler = scheduler_app.scheduler
    assert scheduler
    scheduler.start()

    scheduler.scheduled_job(args=[7], trigger='date', jobstore='sql', executor=executor)(target)

    while process_job_called.value == 0:
        time.sleep(SLEEP_DURATION)

    if USE_REDIS:
        scheduler.scheduled_job(args=[8], trigger='date', jobstore='redis', executor=executor)(target)

        while process_job_called.value == 1:
            time.sleep(SLEEP_DURATION)

    scheduler.shutdown()
    time.sleep(SLEEP_DURATION * 10)

    if remote:
        # noinspection PyUnboundLocalVariable
        p.terminate()
        p.join()

    if USE_REDIS:
        assert process_job_called.value == 2
        assert process_job_call_args[:] == [7, 8]
    else:
        assert process_job_called.value == 1
        assert process_job_call_args[:] == [7, 0]
