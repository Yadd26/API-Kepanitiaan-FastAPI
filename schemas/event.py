from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Skema dasar Task (digunakan di EventResponse)."""
    id: int
    title: str
    description: Optional[str] = None
    status: str
    event_id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    """Skema untuk membuat event baru."""
    title: str = Field(
        ..., min_length=3, max_length=200,
        examples=["Seminar Nasional Teknologi 2026"]
    )
    description: Optional[str] = Field(
        None,
        examples=["Seminar tentang perkembangan AI dan Machine Learning"]
    )
    location: Optional[str] = Field(
        None, max_length=200,
        examples=["Aula Utama Kampus"]
    )
    event_date: datetime = Field(
        ...,
        examples=["2026-05-15T09:00:00"]
    )


class EventUpdate(BaseModel):
    """Skema untuk mengupdate event. Semua field opsional."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    event_date: Optional[datetime] = None


class EventResponse(BaseModel):
    """Skema respons detail event lengkap dengan daftar tasks."""
    id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: datetime
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tasks: List[TaskBase] = []

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(BaseModel):
    """Skema respons event ringkas (tanpa tasks) untuk daftar event."""
    id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: datetime
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
