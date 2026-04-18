"""
SA JobBridge - Database
Uses SQLite so no separate database server is needed.
The file 'jobbridge.db' is created automatically in the project folder.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./jobbridge.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ── Models ──────────────────────────────────────────────────────────────────

class JobListing(Base):
    __tablename__ = "job_listings"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    company     = Column(String(200), nullable=False)
    province    = Column(String(100), nullable=False)
    sector      = Column(String(100))
    skills      = Column(String(500))          # comma-separated
    job_type    = Column(String(50))           # Full-time / Part-time / Contract
    salary_min  = Column(Integer, default=0)
    salary_max  = Column(Integer, default=0)
    description = Column(Text)
    min_edu     = Column(String(100))
    contact     = Column(String(200))
    created_at  = Column(DateTime, default=datetime.utcnow)
    is_active   = Column(Integer, default=1)


class JobSeeker(Base):
    __tablename__ = "job_seekers"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(200), nullable=False)
    email      = Column(String(200))
    phone      = Column(String(50))
    province   = Column(String(100))
    education  = Column(String(100))
    skills     = Column(String(500))           # comma-separated
    job_type   = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class TrainingProgram(Base):
    __tablename__ = "training_programs"

    id             = Column(Integer, primary_key=True, index=True)
    title          = Column(String(200), nullable=False)
    provider       = Column(String(200))
    sector         = Column(String(100))
    duration_weeks = Column(Integer)
    cost           = Column(String(50), default="Free")
    delivery       = Column(String(100))       # Online / In-person
    placement_rate = Column(Float, default=0)
    description    = Column(Text)
    apply_link     = Column(String(500))


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_db():
    """Dependency – yields a DB session, closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables and seed with sample data if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(JobListing).count() == 0:
        _seed_jobs(db)
    if db.query(TrainingProgram).count() == 0:
        _seed_training(db)

    db.close()


def _seed_jobs(db):
    sample_jobs = [
        JobListing(title="Warehouse Picker/Packer", company="PEP Distribution",
                   province="Gauteng", sector="Retail",
                   skills="driving,retail", job_type="Full-time",
                   salary_min=4800, salary_max=5500,
                   description="Pack and sort stock in a busy Gauteng warehouse.",
                   min_edu="Matric / Grade 12", contact="careers@pep.co.za"),
        JobListing(title="Security Guard", company="ADT South Africa",
                   province="Western Cape", sector="Security",
                   skills="security", job_type="Full-time",
                   salary_min=4500, salary_max=5000,
                   description="Guard residential and commercial properties in Cape Town.",
                   min_edu="No matric required", contact="hr@adt.co.za"),
        JobListing(title="Construction Labourer", company="Murray & Roberts",
                   province="KwaZulu-Natal", sector="Construction",
                   skills="construction", job_type="Casual/Contract",
                   salary_min=4200, salary_max=4800,
                   description="General labouring on a large infrastructure project.",
                   min_edu="No matric required", contact="jobs@mur.co.za"),
        JobListing(title="Data Entry Clerk", company="Old Mutual",
                   province="Gauteng", sector="Finance",
                   skills="admin,it", job_type="Full-time",
                   salary_min=6500, salary_max=8000,
                   description="Capture and verify financial records in our Sandton office.",
                   min_edu="Certificate / Diploma", contact="recruit@oldmutual.co.za"),
        JobListing(title="Farm Worker", company="Boland Agri",
                   province="Western Cape", sector="Agriculture",
                   skills="farming", job_type="Full-time",
                   salary_min=4000, salary_max=4500,
                   description="Seasonal fruit-picking and orchard maintenance.",
                   min_edu="No matric required", contact="info@bolandagri.co.za"),
        JobListing(title="Community Health Worker", company="Dept of Health",
                   province="Eastern Cape", sector="Healthcare",
                   skills="care,teaching", job_type="Full-time",
                   salary_min=5200, salary_max=6000,
                   description="Home visits and health education in rural communities.",
                   min_edu="Certificate / Diploma", contact="echealth@gov.za"),
        JobListing(title="Cashier", company="Shoprite Group",
                   province="Gauteng", sector="Retail",
                   skills="retail,sales", job_type="Part-time",
                   salary_min=3500, salary_max=4200,
                   description="Serve customers at tills in a busy Shoprite store.",
                   min_edu="Matric / Grade 12", contact="jobs@shoprite.co.za"),
        JobListing(title="Delivery Driver", company="Checkers",
                   province="Western Cape", sector="Transport",
                   skills="driving", job_type="Full-time",
                   salary_min=6000, salary_max=7000,
                   description="Deliver online orders across Cape Town suburbs.",
                   min_edu="Matric / Grade 12", contact="fleet@checkers.co.za"),
        JobListing(title="IT Support Technician", company="Vodacom",
                   province="Gauteng", sector="IT",
                   skills="it,admin", job_type="Full-time",
                   salary_min=10000, salary_max=14000,
                   description="First-line IT support for corporate clients in Midrand.",
                   min_edu="Certificate / Diploma", contact="it-careers@vodacom.co.za"),
        JobListing(title="Cleaner", company="Bidvest Facilities",
                   province="KwaZulu-Natal", sector="Cleaning",
                   skills="cleaning", job_type="Full-time",
                   salary_min=3400, salary_max=3800,
                   description="Commercial cleaning at office parks in Umhlanga.",
                   min_edu="No matric required", contact="clean@bidvest.co.za"),
        JobListing(title="Kitchen Assistant / Cook", company="Sun International",
                   province="Gauteng", sector="Hospitality",
                   skills="cooking", job_type="Full-time",
                   salary_min=5500, salary_max=6500,
                   description="Assist chefs in a hotel kitchen, Sun City resort.",
                   min_edu="No matric required", contact="food@sun.co.za"),
        JobListing(title="ECD Teacher Assistant", company="Breadline Africa",
                   province="Western Cape", sector="Education",
                   skills="teaching,care", job_type="Part-time",
                   salary_min=3000, salary_max=3500,
                   description="Support early childhood development at community centres.",
                   min_edu="Matric / Grade 12", contact="ecd@breadline.org.za"),
        JobListing(title="Sales Representative", company="Coca-Cola Beverages SA",
                   province="Gauteng", sector="Sales",
                   skills="sales,driving", job_type="Full-time",
                   salary_min=7500, salary_max=10000,
                   description="Manage accounts and grow sales in assigned Gauteng territory.",
                   min_edu="Matric / Grade 12", contact="sales@ccbsa.co.za"),
        JobListing(title="Solar Panel Installer", company="SolarAfrica",
                   province="Western Cape", sector="Energy",
                   skills="construction,it", job_type="Full-time",
                   salary_min=7000, salary_max=9000,
                   description="Install and maintain rooftop solar systems across the Cape.",
                   min_edu="Certificate / Diploma", contact="ops@solarafrica.co.za"),
    ]
    db.bulk_save_objects(sample_jobs)
    db.commit()
    print(f"[Seed] Added {len(sample_jobs)} job listings.")


def _seed_training(db):
    programs = [
        TrainingProgram(title="Digital Literacy & MS Office",
                        provider="MICT SETA", sector="IT",
                        duration_weeks=8, cost="Free", delivery="In-person",
                        placement_rate=85,
                        description="Learn computers, email, Excel and Word from scratch.",
                        apply_link="https://www.mict.org.za"),
        TrainingProgram(title="Construction Skills (NQF 2)",
                        provider="CETA", sector="Construction",
                        duration_weeks=16, cost="Free", delivery="In-person",
                        placement_rate=78,
                        description="Plumbing, tiling, plastering and bricklaying basics.",
                        apply_link="https://www.ceta.org.za"),
        TrainingProgram(title="Agriculture & Food Handling",
                        provider="AgriSETA", sector="Agriculture",
                        duration_weeks=6, cost="Free", delivery="On-site",
                        placement_rate=70,
                        description="Crop management, irrigation and food safety.",
                        apply_link="https://www.agriseta.co.za"),
        TrainingProgram(title="Home-Based Care",
                        provider="Dept of Health / HWSETA", sector="Healthcare",
                        duration_weeks=12, cost="Free", delivery="In-person",
                        placement_rate=80,
                        description="Care for elderly and sick patients at home.",
                        apply_link="https://www.hwseta.org.za"),
        TrainingProgram(title="Retail & Customer Service",
                        provider="W&RSETA", sector="Retail",
                        duration_weeks=4, cost="Free", delivery="In-person",
                        placement_rate=75,
                        description="Cashiering, stock-taking and customer service skills.",
                        apply_link="https://www.wrseta.org.za"),
        TrainingProgram(title="Basic Coding (Python/HTML)",
                        provider="WeThinkCode / WeCode", sector="IT",
                        duration_weeks=24, cost="Free", delivery="In-person",
                        placement_rate=88,
                        description="Beginner software development — no prior experience needed.",
                        apply_link="https://www.wethinkcode.co.za"),
    ]
    db.bulk_save_objects(programs)
    db.commit()
    print(f"[Seed] Added {len(programs)} training programs.")
