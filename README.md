# SA JobBridge — Setup Guide for IntelliJ IDEA

## What you need installed first
- Python 3.10 or newer  →  https://www.python.org/downloads/
- IntelliJ IDEA (Community edition is free)  →  https://www.jetbrains.com/idea/download/

---

## STEP 1 — Open the project in IntelliJ

1. Open IntelliJ IDEA
2. Click  File → Open
3. Navigate to the  sa_jobbridge  folder and click OK
4. IntelliJ will load the project

---

## STEP 2 — Set up a Python interpreter (virtual environment)

1. Go to  File → Project Structure  (or press Ctrl+Alt+Shift+S)
2. Click  SDKs  on the left panel
3. Click the  +  button → Add Python SDK
4. Choose  Virtualenv Environment → New environment
5. Make sure the base interpreter points to your Python 3.10+ installation
6. Click OK, then Apply, then OK

---

## STEP 3 — Open the Terminal inside IntelliJ

At the bottom of IntelliJ click the  Terminal  tab
(or press  Alt+F12 on Windows/Linux  or  Option+F12 on Mac)

You will see a command prompt inside the project folder.

---

## STEP 4 — Install dependencies

In the Terminal, type this command and press Enter:

    pip install -r requirements.txt

Wait for it to finish. You will see packages being downloaded.

---

## STEP 5 — Create a Run Configuration

1. At the top right of IntelliJ click  Add Configuration  (or Edit Configurations)
2. Click the  +  button → select  Python
3. Fill in:
   - Name:         Run SA JobBridge
   - Script path:  (click the folder icon and select  main.py  in your project)
   - Working dir:  (should auto-fill to your project folder)
4. Click OK

---

## STEP 6 — Run the app

1. Click the green  ▶ Play  button at the top right
2. Look at the Run panel at the bottom — you should see:

       SA JobBridge - Starting Server...
       Open your browser: http://localhost:8000
       [Seed] Added 14 job listings.
       [Seed] Added 6 training programs.

3. Open your browser and go to:

       http://localhost:8000

The full platform will open in your browser!

---

## Project file structure

    sa_jobbridge/
    ├── main.py            ← START HERE — runs the server
    ├── app.py             ← wires everything together
    ├── database.py        ← database models + seed data
    ├── requirements.txt   ← Python packages needed
    ├── routes/
    │   ├── jobs.py        ← job listing + matching logic
    │   ├── seekers.py     ← job seeker registration
    │   ├── training.py    ← training programs
    │   └── stats.py       ← SA statistics API
    └── static/
        └── index.html     ← the website (opens in browser)

A file called  jobbridge.db  will be created automatically when you run the app.
This is the SQLite database — do not delete it or your data will be lost.

---

## How to use the platform

| Tab | What it does |
|-----|-------------|
| Job Matcher | Select province, education, skills → get ranked job matches |
| Skills Builder | Browse free SETA training programs |
| Post a Job | Employers post new job listings (saved to the database) |
| Register as Seeker | Job seekers create a profile |
| SA Overview | View unemployment stats and jobs by sector |

---

## API endpoints (for developers)

You can test the backend directly at:

    http://localhost:8000/docs     ← interactive API browser (Swagger UI)
    http://localhost:8000/redoc   ← alternative API docs

Example API calls:
    GET  /api/jobs/                         → list all jobs
    GET  /api/jobs/match?skills=retail,driving&province=Gauteng
    POST /api/jobs/                         → post a new job
    GET  /api/training/                     → list training programs
    GET  /api/stats/overview               → platform statistics

---

## Stopping the server

Press the red  ■ Stop  button in IntelliJ, or press  Ctrl+C  in the Terminal.
