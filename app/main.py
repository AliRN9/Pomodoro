from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import make_aqmp_consumer
from app.infrastructure.broker import get_broker_connection
from app.tasks.handlers import router as task_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_aqmp_consumer()
    yield



app = FastAPI(lifespan=lifespan)

routers = [task_router, user_router, auth_router]
for router in routers:
    app.include_router(router)
