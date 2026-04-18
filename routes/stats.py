"""
SA JobBridge - Statistics Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, JobListing, JobSeeker, TrainingProgram

router = APIRouter()

PROVINCE_UNEMPLOYMENT = {
    "Eastern Cape": 46, "Limpopo": 44, "KwaZulu-Natal": 38,
    "Mpumalanga": 37, "North West": 35, "Free State": 34,
    "Gauteng": 31, "Northern Cape": 30, "Western Cape": 22,
}


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    """Return platform-wide statistics."""
    return {
        "total_jobs":     db.query(JobListing).filter(JobListing.is_active == 1).count(),
        "total_seekers":  db.query(JobSeeker).count(),
        "total_training": db.query(TrainingProgram).count(),
        "national_unemployment_rate": 32.9,
        "province_unemployment": PROVINCE_UNEMPLOYMENT,
    }


@router.get("/jobs-by-province")
def jobs_by_province(db: Session = Depends(get_db)):
    """Count of active jobs per province."""
    from sqlalchemy import func
    rows = (db.query(JobListing.province, func.count(JobListing.id))
              .filter(JobListing.is_active == 1)
              .group_by(JobListing.province)
              .all())
    return {r[0]: r[1] for r in rows}


@router.get("/jobs-by-sector")
def jobs_by_sector(db: Session = Depends(get_db)):
    """Count of active jobs per sector."""
    from sqlalchemy import func
    rows = (db.query(JobListing.sector, func.count(JobListing.id))
              .filter(JobListing.is_active == 1)
              .group_by(JobListing.sector)
              .all())
    return {r[0]: r[1] for r in rows}
