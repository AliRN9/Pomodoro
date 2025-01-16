from dataclasses import dataclass

from repository import TaskCache, TaskRepository
from shema import TaskShema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self):
        if tasks := self.task_cache.get_task():  # достаем из редис
            return tasks

        tasks = self.task_repository.get_tasks()  # достаем из бд
        tasks_schema = [TaskShema.model_validate(task) for task in tasks]
        self.task_cache.set_task(tasks_schema)  # кладем в редис
        return tasks
