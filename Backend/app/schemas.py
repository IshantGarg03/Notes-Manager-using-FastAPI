from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

# For partial update (all fields optional)
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Full note with metadata (response model)
class Note(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2
