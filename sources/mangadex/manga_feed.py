from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

class Attributes(BaseModel):
    volume: Optional[str]
    chapter: str
    title: Optional[str]
    translatedLanguage: str
    externalUrl: Any
    isUnavailable: bool
    publishAt: datetime
    readableAt: datetime
    createdAt: datetime
    updatedAt: datetime
    pages: int
    version: int


class Relationship(BaseModel):
    id: str
    type: str


class Datum(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: List[Relationship]


class Model(BaseModel):
    result: str
    response: str
    data: List[Datum]
    limit: int
    offset: int
    total: int
