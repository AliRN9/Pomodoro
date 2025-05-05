from typing import Optional

from pydantic import BaseModel, Field, model_validator, ConfigDict


class TaskShema(BaseModel):
    id: int = Field(exclude=True, default=None)
    name: Optional[str] = None
    pomodoro_count: Optional[int] = None
    category_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def check_name_or_count(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Task name or pomodoro count must be set")
        return self


class TaskCreateShema(BaseModel):
    name: Optional[str] = None
    pomodoro_count: Optional[int] = None
    category_id: int = Field(alias='category_id')
