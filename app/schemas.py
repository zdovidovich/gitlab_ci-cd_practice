from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=150)
    year: int | None = Field(None, ge=1000, le=2100)
    is_read: bool = False


class BookCreate(BookBase):
    """Схема для создания книги (входные данные)."""
    pass


class BookUpdate(BaseModel):
    """Схема для обновления книги (все поля опциональны)."""
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=150)
    year: int | None = Field(None, ge=1000, le=2100)
    is_read: bool | None = None


class BookResponse(BookBase):
    """Схема для ответа API (с id и датой создания)."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
