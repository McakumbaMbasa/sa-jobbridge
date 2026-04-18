"""
SA JobBridge - Job Seekers Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db, JobSeeker

router = APIRouter()


class SeekerCreate(BaseModel):
    name: str
    email: Optional[str] = ""
    phone: Optional[str] = ""
    province: Optional[str] = ""
    education: Optional[str] = ""
    skills: Optional[str] = ""
    job_type: Optional[str] = "Any"


class SeekerOut(SeekerCreate):
    id: int
    class Config:
        from_attributes = True


@router.post("/", response_model=SeekerOut, status_code=201)
def register_seeker(payload: SeekerCreate, db: Session = Depends(get_db)):
    """Register a new job seeker."""
    seeker = JobSeeker(**payload.dict())
    db.add(seeker)
    db.commit()
    db.refresh(seeker)
    return seeker


@router.get("/", response_model=List[SeekerOut])
def list_seekers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(JobSeeker).offset(skip).limit(limit).all()


@router.get("/{seeker_id}", response_model=SeekerOut)
def get_seeker(seeker_id: int, db: Session = Depends(get_db)):
    s = db.query(JobSeeker).filter(JobSeeker.id == seeker_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Seeker not found")
    return s
