import json

from redis import Redis

from shema.task import TaskShema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_task(self) -> list[TaskShema]:
        with self.redis as redis:
            tasks_json = redis.lrange('tasks', 0, -1)

            return [TaskShema.model_validate(json.loads(task)) for task in tasks_json]

    def set_task(self, tasks: list[TaskShema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        if tasks_json:
            with self.redis as redis:
                redis.lpush("tasks", *tasks_json)
                redis.expire("tasks", 30)
