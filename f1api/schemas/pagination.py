from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    items: list[T] = Field(..., description="List of items in current page")
    total: int = Field(..., description="Total number of items available")
    limit: int = Field(..., description="Maximum items per page")
    offset: int = Field(..., description="Number of items skipped")
    page: int = Field(..., description="Current page number (1-indexed)")
    pages: int = Field(..., description="Total number of pages")

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        limit: int,
        offset: int,
    ) -> "PaginatedResponse[T]":
        """Helper to create paginated response with calculated fields."""
        page = (offset // limit) + 1 if limit > 0 else 1
        pages = (total + limit - 1) // limit if limit > 0 else 1
        return cls(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
            page=page,
            pages=pages,
        )
