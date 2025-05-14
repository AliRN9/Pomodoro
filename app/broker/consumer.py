import json
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer

    async def open_connection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        await self.open_connection()
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        try:
            async for message in self.consumer:
                print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
                print(f"{message.value=}")
        except Exception as e:
            print(e)
        finally:
            await self.close_connection()

#
# from app.infrastructure.broker import get_broker_connection
# import aio_pika
#
#
# async def make_aqmp_consumer():
#     connection = await get_broker_connection()
#     channel = await connection.channel()
#     # await channel.declare_queue("callback_email_queue", durable=True)
#     queue = await channel.declare_queue("callback_email_queue", durable=True)
#     # await queue.consume(consume_fail_email)
#
#
# async def consume_fail_email(message: aio_pika.abc.AbstractIncomingMessage):
#     async with message.process():
#         email_body = message.body.decode()
#         correlation_id = message.correlation_id
#         print(f"{email_body=}", f"{correlation_id=}")
