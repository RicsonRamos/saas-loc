from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageMeta(BaseModel):
    page: int
    limit: int
    total: int


class Page(BaseModel, Generic[T]):
    data: list[T]
    meta: PageMeta
