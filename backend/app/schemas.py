from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileRead(BaseModel):
    id: int
    name: str
    file_url: str
    file_size: int
    file_type: str
    category: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    pages: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
