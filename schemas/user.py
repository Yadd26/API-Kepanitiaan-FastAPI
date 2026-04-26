from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Skema untuk registrasi user baru."""
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    email: str = Field(..., max_length=100, examples=["john@example.com"])
    password: str = Field(..., min_length=6, examples=["secret123"])


class UserResponse(BaseModel):
    """Skema respons data user (tanpa password)."""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Skema respons token JWT."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data yang disimpan di dalam token JWT."""
    username: Optional[str] = None


class UserLogin(BaseModel):
    """Skema untuk login user."""
    username: str = Field(..., examples=["johndoe"])
    password: str = Field(..., examples=["secret123"])
