import json

# from redis import Redis
from redis import asyncio as redis
from app.tasks.shema import TaskShema


class TaskCache:
    def __init__(self, redis: redis.Redis):
        self.redis = redis

    async def get_task(self) -> list[TaskShema]:
        async with self.redis as redis:
            tasks_json = await redis.lrange('tasks', 0, -1)

            return [TaskShema.model_validate(json.loads(task)) for task in tasks_json]

    async def set_task(self, tasks: list[TaskShema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        if tasks_json:
            async with self.redis as redis:
                await redis.lpush("tasks", *tasks_json)
                await redis.expire("tasks", 30)
