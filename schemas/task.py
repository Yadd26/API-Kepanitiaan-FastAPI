from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Skema untuk membuat task baru."""
    title: str = Field(
        ..., min_length=3, max_length=200,
        examples=["Siapkan spanduk acara"]
    )
    description: Optional[str] = Field(
        None,
        examples=["Desain dan cetak spanduk ukuran 3x1 meter"]
    )
    status: Optional[str] = Field(
        "pending",
        examples=["pending"]
    )
    event_id: int = Field(..., examples=[1])
    assigned_to: Optional[int] = Field(None, examples=[1])


class TaskUpdate(BaseModel):
    """Skema untuk mengupdate task. Semua field opsional."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(
        None,
        description="Status task: pending, in_progress, atau done"
    )
    assigned_to: Optional[int] = None


class TaskResponse(BaseModel):
    """Skema respons detail task."""
    id: int
    title: str
    description: Optional[str] = None
    status: str
    event_id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
