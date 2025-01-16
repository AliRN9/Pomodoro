from pydantic import BaseModel, Field, model_validator


class TaskShema(BaseModel):
    id: int = Field(include=False,default=None)
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int = Field(alias='category_id')

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_name_or_count(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Task name or pomodoro count must be set")
        return self
