import aio_pika
import pytest

from dropland.engines.rmq import USE_RMQ

pytestmark = pytest.mark.skipif(not USE_RMQ, reason='For RabbitMQ only')

if USE_RMQ:
    from dropland.engines.rmq.containers import RmqContainer, SingleRmqContainer, MultipleRmqContainer
    from dropland.engines.rmq import EngineConfig, RmqEngine
    from tests import RMQ_URI


@pytest.mark.asyncio
async def test_create_engine():
    default_rmq_storage = RmqContainer()
    engine_factory = default_rmq_storage.engine_factory()

    assert not engine_factory.get_engine('')

    config = EngineConfig(url=RMQ_URI)
    assert engine_factory.create_engine('dropland', config)

    engine = engine_factory.get_engine('dropland')
    assert engine
    assert engine.backend is engine_factory
    assert engine.is_async

    assert engine_factory.get_engine_names() == ['dropland']


@pytest.mark.asyncio
async def test_create_connection():
    default_rmq_storage = RmqContainer()
    engine_factory = default_rmq_storage.engine_factory()

    config = EngineConfig(url=RMQ_URI)
    engine = engine_factory.create_engine('dropland', config)

    assert engine
    await engine.start()

    async with engine.session() as channel:
        queue = await channel.declare_queue('test', auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=b'12345'),
            routing_key='test',
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    assert message.body == b'12345'
                break

    await engine.stop()


@pytest.mark.asyncio
async def test_storage_container():
    config = EngineConfig(url=RMQ_URI)

    cont = RmqContainer()

    eng = cont.create_engine('dropland', config)
    assert isinstance(eng, RmqEngine)
    assert eng.name == 'dropland'
    cont.unwire()

    cont = SingleRmqContainer()
    cont.config.from_dict({
        'name': '_',
        'engine_config': config
    })
    eng1 = cont.create_engine()
    eng2 = cont.create_engine()
    assert eng1.name == eng2.name == '_'
    assert eng1 is eng2
    cont.unwire()

    cont = MultipleRmqContainer()
    cont.config.from_dict({
        'one': {
            'engine_config': config
        },
        'two': {
            'engine_config': config
        },
    })

    eng1 = cont.create_engine('one')
    eng2 = cont.create_engine('two')
    assert eng1 is not eng2
    assert eng1.is_async is True
    assert eng2.is_async is True
    assert eng1.name == 'one'
    assert eng2.name == 'two'

    cont.unwire()
