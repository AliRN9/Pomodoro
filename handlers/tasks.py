from fastapi import HTTPException
from typing import List, Annotated

from fastapi import APIRouter, status, Depends

from dependecy import get_tasks_repository, get_tasks_service, get_request_user_id
from exception import TaskNotFound
from repository import TaskRepository, TaskCache
from service import TaskService
from shema import TaskShema, TaskCreateShema

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=List[TaskShema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)],
                    user_id: int = Depends(get_request_user_id)
                    ):
    return task_service.get_tasks(user_id=user_id)


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
    task = task_service.create_task(body, user_id)
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
        return task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
