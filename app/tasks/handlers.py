import time

from fastapi import HTTPException
from typing import List, Annotated

from fastapi import APIRouter, status, Depends, BackgroundTasks
import asyncio
from app.dependecy import get_tasks_service, get_request_user_id
from app.exception import TaskNotFound
from app.tasks.service import TaskService
from app.tasks.shema import TaskShema, TaskCreateShema

router = APIRouter(prefix="/task", tags=["task"])


async def get_tasks_log(tasks_count: int):
    await asyncio.sleep(1)
    print(f"tasks_count: {tasks_count}")

@router.get("/test_all", response_model=List[TaskShema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)],
                    background_tasks: BackgroundTasks,
                    ):
    tasks = await task_service.get_all_tasks()
    background_tasks.add_task(get_tasks_log, tasks_count=len(tasks))
    return tasks




@router.get("/all", response_model=List[TaskShema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)],
                    user_id: int = Depends(get_request_user_id),
                    ):
    tasks = await task_service.get_tasks(user_id=user_id)
    return tasks


# @router.get("/{task_id}", response_model=TaskShema)
# async def get_task(task_id: int,
#                    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
#                    ):
#     task = task_repository.get_task(task_id)
#     return task


@router.post("/", response_model=TaskShema)
async def create_task(
        body: TaskCreateShema,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
) -> TaskShema:
    task = await task_service.create_task(body, user_id)
    return task


@router.patch("/{task_id}", response_model=TaskShema)
async def update_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    # task = next((task for task in fixture_tasks if task["id"] == task_id), None)
    try:
        return await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
