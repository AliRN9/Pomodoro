from fastapi import HTTPException
from typing import List, Annotated

from fastapi import APIRouter, status, Depends

from dependecy import get_tasks_repository, get_tasks_cache_repository, get_tasks_service
from repository import TaskRepository, TaskCache
from service import TaskService
from shema.task import TaskShema

router = APIRouter(prefix="/tasks", tags=["task"])


@router.get("/all", response_model=List[TaskShema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)],
                    ):
    return task_service.get_tasks()


@router.get("/{task_id}", response_model=TaskShema)
async def get_task(task_id: int,
                   task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
                   ):
    task = task_repository.get_task(task_id)
    return task

@router.post("/", response_model=TaskShema)
async def create_task(
        task: TaskShema,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task.id = task_repository.create_task(task)
    return task


@router.patch("/{task_id}", response_model=TaskShema)
async def update_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    # task = next((task for task in fixture_tasks if task["id"] == task_id), None)

    return task_repository.update_task_name(task_id,name)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_repository.delete_task(task_id)

    return {"message": 'deleted'}
