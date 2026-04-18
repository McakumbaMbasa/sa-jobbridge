"""
SA JobBridge - Training Routes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db, TrainingProgram

router = APIRouter()


class TrainingOut(BaseModel):
    id: int
    title: str
    provider: Optional[str]
    sector: Optional[str]
    duration_weeks: Optional[int]
    cost: Optional[str]
    delivery: Optional[str]
    placement_rate: Optional[float]
    description: Optional[str]
    apply_link: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[TrainingOut])
def list_training(
    sector: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all training programs, optionally filtered by sector."""
    q = db.query(TrainingProgram)
    if sector:
        q = q.filter(TrainingProgram.sector == sector)
    return q.order_by(TrainingProgram.placement_rate.desc()).all()
