from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteOut

router = APIRouter()


@router.get("/notes", response_model=List[NoteOut])
def get_notes(
    subject: Optional[str] = Query(None, description="Filter by subject name"),
    db: Session = Depends(get_db)
):
    """Get all notes, optionally filtered by subject."""
    query = db.query(Note)
    if subject:
        query = query.filter(Note.subject.ilike(f"%{subject}%"))
    notes = query.order_by(Note.created_at.desc()).all()

    result = []
    for note in notes:
        note_dict = {
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "subject": note.subject,
            "subject_code": note.subject_code,
            "file_url": note.file_url,
            "file_type": note.file_type,
            "uploaded_by": note.uploaded_by,
            "uploader_name": note.uploader.name if note.uploader else "Faculty",
            "created_at": note.created_at,
        }
        result.append(note_dict)
    return result


@router.post("/notes", response_model=NoteOut)
def create_note(data: NoteCreate, uploader_id: int = Query(..., description="User ID of faculty posting"), db: Session = Depends(get_db)):
    """Faculty posts a new note with a Google Drive / external link."""
    from app.models.user import User
    uploader = db.query(User).filter(User.id == uploader_id).first()
    if not uploader:
        raise HTTPException(status_code=404, detail="Uploader user not found.")
    if uploader.role not in ('faculty', 'hod'):
        raise HTTPException(status_code=403, detail="Only faculty or HOD can upload notes.")

    note = Note(
        title=data.title,
        description=data.description,
        subject=data.subject,
        subject_code=data.subject_code,
        file_url=data.file_url,
        file_type=data.file_type or "pdf",
        uploaded_by=uploader_id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return {
        "id": note.id, "title": note.title, "description": note.description,
        "subject": note.subject, "subject_code": note.subject_code,
        "file_url": note.file_url, "file_type": note.file_type,
        "uploaded_by": note.uploaded_by,
        "uploader_name": note.uploader.name if note.uploader else "Faculty",
        "created_at": note.created_at
    }


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note by ID."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully."}
