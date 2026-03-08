from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    subject_code: Optional[str] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = "pdf"


class NoteOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    subject: str
    subject_code: Optional[str]
    file_url: Optional[str]
    file_type: str
    uploaded_by: int
    uploader_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
