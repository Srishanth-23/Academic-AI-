from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    code: str
    faculty_id: int


class SubjectResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True