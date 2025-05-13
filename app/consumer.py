import json

from app.infrastructure.broker import get_broker_connection
import aio_pika


async def make_aqmp_consumer():
    connection = await get_broker_connection()
    channel = await connection.channel()
    # await channel.declare_queue("callback_email_queue", durable=True)
    queue = await channel.declare_queue("callback_email_queue", durable=True)
    await queue.consume(consume_fail_email)


async def consume_fail_email(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        email_body = message.body.decode()
        correlation_id = message.correlation_id
        print(f"{email_body=}", f"{correlation_id=}")
