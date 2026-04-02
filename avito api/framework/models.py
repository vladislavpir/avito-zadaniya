from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatisticsModel(BaseModel):
    likes: int
    contacts: int
    viewCount: int


class ItemModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    createdAt: str
    id: UUID
    name: str
    price: int
    sellerId: int
    statistics: StatisticsModel


class StatisticsResponseEntryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contacts: int
    likes: int
    viewCount: int


class ErrorResultModel(BaseModel):
    message: str
    messages: dict[str, Any] | None


class ErrorResponseModel(BaseModel):
    result: ErrorResultModel
    status: str


class CreateItemResponseModel(BaseModel):
    status: str
