from typing import Any, Optional

from sqlalchemy.orm import declarative_base, Mapped, mapped_column, DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()




class Tasks(Base):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=False)


class Categories(Base):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    type:  Mapped[Optional[str]] # либо так mapped_column(nullable=True)
    name: Mapped[str]
