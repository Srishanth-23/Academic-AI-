from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    unique_id: str
    department: Optional[str] = None
    section_id: Optional[int] = None
    is_class_advisor: Optional[bool] = False
    class_advisor_for_section_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str