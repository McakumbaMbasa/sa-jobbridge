"""
SA JobBridge - Main Entry Point
Run this file to start the application
"""

from app import create_app

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  SA JobBridge - Starting Server...")
    print("  Open your browser: http://localhost:8000")
    print("=" * 50)
    uvicorn.run("app:create_app", host="0.0.0.0", port=8000, reload=True, factory=True)
