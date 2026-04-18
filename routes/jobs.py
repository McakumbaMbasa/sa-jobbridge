"""
SA JobBridge - Jobs Routes
Handles listing, searching, posting, and matching jobs.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db, JobListing

router = APIRouter()


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class JobCreate(BaseModel):
    title: str
    company: str
    province: str
    sector: Optional[str] = ""
    skills: Optional[str] = ""
    job_type: Optional[str] = "Full-time"
    salary_min: Optional[int] = 0
    salary_max: Optional[int] = 0
    description: Optional[str] = ""
    min_edu: Optional[str] = "No matric required"
    contact: Optional[str] = ""


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    province: str
    sector: Optional[str]
    skills: Optional[str]
    job_type: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: Optional[str]
    min_edu: Optional[str]
    contact: Optional[str]
    match_score: Optional[float] = None

    class Config:
        from_attributes = True


# ── Matching helper ───────────────────────────────────────────────────────────

EDU_RANK = {
    "no matric required": 0,
    "matric / grade 12": 1,
    "certificate / diploma": 2,
    "degree": 3,
    "postgraduate": 4,
}


def compute_match(job: JobListing, seeker_skills: List[str],
                  seeker_province: str, seeker_edu: str,
                  seeker_job_type: str) -> float:
    score = 0.0

    # Skill overlap (50 pts)
    job_skills = [s.strip().lower() for s in (job.skills or "").split(",") if s.strip()]
    if job_skills and seeker_skills:
        matched = len(set(seeker_skills) & set(job_skills))
        score += (matched / len(job_skills)) * 50

    # Province match (20 pts)
    if seeker_province and job.province.lower() == seeker_province.lower():
        score += 20

    # Education eligibility (20 pts)
    user_rank = EDU_RANK.get(seeker_edu.lower(), 5)
    req_rank = EDU_RANK.get((job.min_edu or "").lower(), 0)
    if user_rank >= req_rank:
        score += 20

    # Job type (10 pts)
    if not seeker_job_type or seeker_job_type.lower() in ("any", job.job_type.lower()):
        score += 10

    return round(score, 1)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[JobOut])
def list_jobs(
    province: Optional[str] = None,
    sector:   Optional[str] = None,
    job_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Return all active job listings, optionally filtered."""
    q = db.query(JobListing).filter(JobListing.is_active == 1)
    if province:
        q = q.filter(JobListing.province == province)
    if sector:
        q = q.filter(JobListing.sector == sector)
    if job_type:
        q = q.filter(JobListing.job_type == job_type)
    return q.offset(skip).limit(limit).all()


@router.get("/match", response_model=List[JobOut])
def match_jobs(
    skills:   str = Query("", description="Comma-separated skills e.g. driving,retail"),
    province: str = Query("", description="Province name"),
    education: str = Query("", description="Education level"),
    job_type: str = Query("Any", description="Full-time / Part-time / Casual/Contract / Any"),
    db: Session = Depends(get_db)
):
    """Return jobs ranked by match score for a job seeker's profile."""
    seeker_skills = [s.strip().lower() for s in skills.split(",") if s.strip()]

    jobs = db.query(JobListing).filter(JobListing.is_active == 1).all()

    results = []
    for job in jobs:
        score = compute_match(job, seeker_skills, province, education, job_type)
        if score > 0:
            job_out = JobOut(
                id=job.id, title=job.title, company=job.company,
                province=job.province, sector=job.sector, skills=job.skills,
                job_type=job.job_type, salary_min=job.salary_min,
                salary_max=job.salary_max, description=job.description,
                min_edu=job.min_edu, contact=job.contact, match_score=score
            )
            results.append(job_out)

    results.sort(key=lambda j: j.match_score, reverse=True)
    return results[:10]


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job by ID."""
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobOut, status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    """Post a new job listing."""
    job = JobListing(**payload.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def deactivate_job(job_id: int, db: Session = Depends(get_db)):
    """Soft-delete a job (sets is_active = 0)."""
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.is_active = 0
    db.commit()
    return {"message": f"Job {job_id} deactivated."}
