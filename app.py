"""
SA JobBridge - App Factory
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from database import init_db
from routes import jobs, seekers, training, stats


def create_app() -> FastAPI:
    app = FastAPI(
        title="SA JobBridge",
        description="Solving unemployment in South Africa",
        version="1.0.0"
    )

    # Allow browser requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialise database on startup
    @app.on_event("startup")
    def startup():
        init_db()
        print("[SA JobBridge] Database ready.")

    # Register route groups
    app.include_router(jobs.router,     prefix="/api/jobs",     tags=["Jobs"])
    app.include_router(seekers.router,  prefix="/api/seekers",  tags=["Job Seekers"])
    app.include_router(training.router, prefix="/api/training", tags=["Training"])
    app.include_router(stats.router,    prefix="/api/stats",    tags=["Statistics"])

    # Serve the frontend
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app
