import aio_pika.abc

from app.settings import settings


async def get_broker_connection() -> aio_pika.abc.AbstractConnection:
    return await aio_pika.connect_robust(settings.AMQP_URL)
