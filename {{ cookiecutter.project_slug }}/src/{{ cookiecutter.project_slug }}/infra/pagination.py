from typing import TypeVar

from pydantic import BaseModel, Field
from sqlalchemy.sql import func
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar

T = TypeVar("T", bound=SQLModel)

MAX_RESULTS_PER_PAGE = 50


class PaginationParams(BaseModel):
    page_number: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=MAX_RESULTS_PER_PAGE)


class Page[T](BaseModel):
    records: list[T] = Field()
    total_row: int = Field(ge=0)
    total_page: int = Field(ge=0)
    page_number: int = Field(ge=0)
    page_size: int = Field(ge=0)


async def paginate(
    session: AsyncSession,
    query: SelectOfScalar[T],
    params: PaginationParams,
) -> Page[T]:
    total_row = await session.scalar(select(func.count()).select_from(query.subquery()))
    if not isinstance(total_row, int):
        raise RuntimeError("A database error occurred when getting `total_row`.")

    total_pages = (total_row + params.page_size - 1) // params.page_size
    total_pages = max(total_pages, 1)
    current_page = min(params.page_number, total_pages)
    offset = (current_page - 1) * params.page_size

    result = await session.exec(query.offset(offset).limit(params.page_size))
    items = list(result.all())

    return Page[T](
        records=items,
        total_row=total_row,
        total_page=total_pages,
        page_size=len(items),
        page_number=current_page,
    )
