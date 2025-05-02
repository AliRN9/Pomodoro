from fastapi import FastAPI
from app.tasks.handlers import router as task_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router

app = FastAPI()

routers = [task_router, user_router, auth_router]
for router in routers:
    app.include_router(router)
