import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.dependecy import get_broker_consumer
# from app.broker import make_aqmp_consumer
from app.tasks.handlers import router as task_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # await make_aqmp_consumer()
#
#     consumer = await get_broker_consumer()
#     await consumer.consume_callback_message()
#     yield

async def lifespan(app: FastAPI):
    consumer = await get_broker_consumer()
    task = asyncio.create_task(consumer.consume_callback_message())  # НЕ блокируем здесь
    yield
    await consumer.close_connection()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass



app = FastAPI(lifespan=lifespan)

routers = [task_router, user_router, auth_router]
for router in routers:
    app.include_router(router)
