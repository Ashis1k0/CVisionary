# CVisionary Feature Tracker

This document tracks features that existed in the project originally and features added in recent updates.

---

## 1) Original/Core Features (Before Recent Enhancements)

### Resume Processing and AI Analysis
- Resume upload (`PDF`, `DOCX`)
- Resume text extraction (PyPDF2 + DOCX parser)
- OCR fallback for scanned documents
- Gemini-based resume parsing
- Structured extraction:
  - name, email, phone
  - skills
  - education
  - experience
  - projects
  - location

### ATS and Career Support
- ATS score calculation (`0-100`)
- Resume improvement suggestions (Gemini)
- AI job recommendations (Gemini)
- Downloadable PDF report of resume analysis

### Candidate and Admin Management
- Candidate profile persistence in MySQL (SQLAlchemy)
- Admin login/logout
- User register/login/logout
- Admin dashboard to inspect candidate resume details
- Candidate shortlist (ATS-based)
- Advanced shortlist filters:
  - ATS score
  - CGPA
  - academic percentage
  - graduation year
  - skills
  - upload date range
- Candidate search
- CSV export (shortlist/search/advanced shortlist)
- Resume statistics dashboard

---

## 2) New Features Added (Current)

### Voice AI Mock Interview System
- Voice interview page
- AI-generated interview questions (Gemini)
- Microphone input using Web Speech API
- Speech-to-text transcript capture
- Gemini answer evaluation:
  - score (0-10)
  - feedback
  - improvement tips
- Interview loop handling:
  - start
  - get question
  - submit answer
  - finish/force end
- Final interview result page
- Admin interview sessions page

### Recruiter and Job Posting Platform
- Recruiter model and authentication:
  - register
  - login
  - dashboard
  - logout
- Job post model
- Recruiter job operations:
  - create
  - list (my jobs)
  - edit
  - delete
- Recruiter applications view

### Candidate Job Discovery and Applications
- Jobs Board page
- Search jobs by role/skills/company (`q`)
- Resume-based suggested jobs after upload
- Match score = overlapping skill count
- Candidate apply flows:
  - redirect-based apply
  - AJAX apply (no page refresh)
- Candidate applied-jobs tracking page (`/jobs/applied`)

### UI/UX Enhancements Added
- Persistent recruiter navigation tabs:
  - Overview
  - New Job
  - My Jobs
  - Applications
- Main page quick links:
  - Apply Jobs
  - My Applied Jobs (for logged-in user)
  - Recruiter Login
- Suggested jobs apply button becomes `Applied` after success
- Toast notifications for apply success/error
- Admin resume detail modal made scrollable
- Voice interview admin tab added consistently across admin pages

### Seed and Bootstrapping
- `seed_data.py` added
- Auto-seeding (when empty) for:
  - default recruiter (`recruiter@test.com`)
  - sample jobs

---

## 3) New Data Entities Added

- `interview_sessions`
- `recruiters`
- `job_posts`
- `job_applications`

---

## 4) High-Level Change Summary by Module

### Routes
- Added/extended:
  - `routes/interview_voice_routes.py`
  - `routes/recruiter_routes.py`
  - `routes/job_routes.py`

### Services
- Added:
  - `services/voice_interview_ai.py`
  - `services/job_matcher.py`

### Templates
- Added:
  - `voice_interview.html`
  - `voice_interview_result.html`
  - `admin_interviews.html`
  - `recruiter_login.html`
  - `recruiter_register.html`
  - `recruiter_dashboard.html`
  - `recruiter_job_create.html`
  - `recruiter_job_edit.html`
  - `recruiter_jobs.html`
  - `recruiter_applications.html`
  - `jobs_board.html`
  - `candidate_applied_jobs.html`

### Existing Files Updated
- `app.py`
- `static/js/main.js`
- `templates/index.html`
- admin templates (navigation + modal UX updates)
- documentation files:
  - `README.md`
  - `SRS_Document.md`
  - `System_Design.md`
  - `Database_Schema_Design.md`

---

## 5) Notes for Future Tracking

For each future release, append:
- date/version
- added features
- updated features
- removed/deprecated features
- impacted files

