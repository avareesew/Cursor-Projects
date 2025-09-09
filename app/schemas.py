from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ContestantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    bio: Optional[str] = Field(None, max_length=2000)


class ContestantCreate(ContestantBase):
    pass


class ContestantOut(ContestantBase):
    id: int

    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    picks: List[int] = Field(..., min_items=1)


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionOut(SubmissionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
