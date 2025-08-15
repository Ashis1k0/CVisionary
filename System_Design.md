# System Design Document
## CVisionary - AI-Powered Resume Analysis System

**Version:** 1.0  
**Date:** August 2025  
**Project:** CVisionary  
**Document Type:** System Design Document

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Component Design](#3-component-design)
4. [Data Flow Design](#4-data-flow-design)
5. [API Design](#5-api-design)
6. [Security Design](#6-security-design)
7. [Performance Considerations](#7-performance-considerations)
8. [Scalability Strategy](#8-scalability-strategy)
9. [Error Handling](#9-error-handling)
10. [Monitoring and Logging](#10-monitoring-and-logging)
11. [Deployment Strategy](#11-deployment-strategy)

---

## 1. Introduction

### 1.1 Purpose
This document provides a comprehensive system design for CVisionary, detailing the architecture, components, data flow, and technical implementation of the AI-powered resume analysis system.

### 1.2 System Overview
CVisionary is a web-based application that provides intelligent resume analysis using Google's Gemini AI, ATS scoring, job recommendations, and candidate management features for HR professionals.

### 1.3 Key Design Principles
- **Modularity**: Separate concerns into distinct components
- **Scalability**: Design for future growth and increased load
- **Security**: Implement robust authentication and data protection
- **Performance**: Optimize for fast response times and efficient processing
- **Maintainability**: Clean, well-documented code structure

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Browser   │  │   Mobile    │  │   Tablet    │          │
│  │   (Web)     │  │   Browser   │  │   Browser   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   HTML5     │  │    CSS3     │  │ JavaScript  │          │
│  │ Templates   │  │  Styling    │  │  Bootstrap  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Flask     │  │  Business   │  │   Session   │          │
│  │   Web App   │  │   Logic     │  │ Management  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Service Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   AI/ML     │  │ Document    │  │   Export    │          │
│  │  Services   │  │ Processing  │  │  Services   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   MySQL     │  │   File      │  │   SQLAlchemy│          │
│  │  Database   │  │  Storage    │  │     ORM     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                            │
├─────────────────────────────────────────────────────────────────┤
│  Google Gemini AI  │  Email Service  │  Backup Service         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python 3.11+, Flask 2.0.1
- **Database**: MySQL 8.0+, SQLAlchemy 2.0.25
- **AI/ML**: Google Gemini AI, NLTK, Scikit-learn
- **Document Processing**: PyPDF2, python-docx, pytesseract
- **File Storage**: Local file system
- **Session Management**: Flask sessions

### 2.3 System Components
1. **Web Application Server** (Flask)
2. **AI Processing Engine** (Google Gemini AI)
3. **Document Processing Engine** (Multi-format support)
4. **Database Management System** (MySQL + SQLAlchemy)
5. **File Storage System** (Local file system)
6. **User Authentication System** (Flask sessions)

---

## 3. Component Design

### 3.1 Web Application Server (Flask)

#### 3.1.1 Core Components
```python
# Main Flask Application Structure
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.secret_key = '20233952'
```

#### 3.1.2 Route Structure
```python
# Main Routes
@app.route('/')                    # Home page
@app.route('/upload', methods=['POST'])  # Resume upload
@app.route('/admin-login')         # Admin authentication
@app.route('/admin-page')          # Admin dashboard
@app.route('/candidate-shortlist') # Candidate management
@app.route('/advanced-shortlist')  # Advanced filtering
@app.route('/resume-statistics')   # Analytics dashboard
```

#### 3.1.3 Session Management
```python
# Session-based authentication
session['admin_logged_in'] = True
session['admin_username'] = admin.username
session['user_logged_in'] = True
session['username'] = user.username
```

### 3.2 AI Processing Engine

#### 3.2.1 Google Gemini AI Integration
```python
# AI Configuration
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Resume Parsing Function
def parse_resume_with_gemini(file_path):
    # Text extraction
    # AI processing
    # Structured data extraction
    # JSON response formatting
```

#### 3.2.2 AI Processing Pipeline
```
1. Document Upload → File Validation
2. Text Extraction → OCR (if needed)
3. AI Processing → Gemini AI Analysis
4. Data Structuring → JSON Format
5. Score Calculation → ATS Scoring
6. Recommendations → Job Matching
```

### 3.3 Document Processing Engine

#### 3.3.1 Multi-format Support
```python
# PDF Processing
def extract_text_from_pdf(pdf_path):
    # PyPDF2 extraction
    # OCR fallback
    # Error handling

# DOCX Processing
def extract_text_from_docx(docx_path):
    # python-docx extraction
    # Image OCR support
    # Error handling
```

#### 3.3.2 OCR Integration
```python
# Tesseract OCR for scanned documents
import pytesseract
from pdf2image import convert_from_path

def ocr_fallback(file_path):
    # Convert PDF to images
    # OCR processing
    # Text extraction
```

### 3.4 Database Management System

#### 3.4.1 SQLAlchemy ORM Models
```python
# Database Models
class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class CandidateProfile(Base):
    __tablename__ = 'candidate_profiles'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    skills = Column(Text)  # JSON string
    education = Column(Text)  # JSON string
    experience = Column(Text)  # JSON string
    projects = Column(Text)  # JSON string
    ats_score = Column(Integer, default=0)
    # ... additional fields
```

#### 3.4.2 Database Connection
```python
# Database Configuration
engine = create_engine("mysql://root:root10@localhost/resume_analysis")
Session = sessionmaker(bind=engine)
sqlalchemy_session = Session()
```

### 3.5 File Storage System

#### 3.5.1 File Upload Management
```python
# File Upload Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Secure File Handling
def secure_file_upload(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath
```

#### 3.5.2 File Organization
```
uploads/
├── resumes/
│   ├── pdf/
│   └── docx/
├── processed/
└── exports/
```

---

## 4. Data Flow Design

### 4.1 Resume Upload and Processing Flow
```
1. User Uploads Resume
   ↓
2. File Validation (Size, Format)
   ↓
3. Secure File Storage
   ↓
4. Text Extraction (PDF/DOCX)
   ↓
5. AI Processing (Gemini AI)
   ↓
6. Data Structuring (JSON)
   ↓
7. ATS Score Calculation
   ↓
8. Database Storage
   ↓
9. Response to User
```

### 4.2 User Authentication Flow
```
1. User Login Request
   ↓
2. Credential Validation
   ↓
3. Session Creation
   ↓
4. Role-based Access Control
   ↓
5. Dashboard Redirect
```

### 4.3 Admin Management Flow
```
1. Admin Login
   ↓
2. Dashboard Access
   ↓
3. Candidate Data Retrieval
   ↓
4. Filtering and Search
   ↓
5. Data Export
   ↓
6. Analytics Generation
```

### 4.4 AI Processing Flow
```
1. Text Input to Gemini AI
   ↓
2. Structured Prompt Generation
   ↓
3. AI Response Processing
   ↓
4. JSON Parsing and Validation
   ↓
5. Data Normalization
   ↓
6. Score Calculation
   ↓
7. Recommendation Generation
```

---

## 5. API Design

### 5.1 RESTful API Endpoints

#### 5.1.1 Resume Processing APIs
```python
# Upload Resume
POST /upload
Content-Type: multipart/form-data
Parameters: resume (file)
Response: JSON with parsed data and scores

# Get ATS Score
POST /ats-score
Content-Type: application/json
Parameters: parsed_data (JSON)
Response: JSON with score

# Job Recommendations
POST /job-recommendations
Content-Type: application/json
Parameters: skills (array)
Response: JSON with job recommendations
```

#### 5.1.2 Admin Management APIs
```python
# Admin Login
POST /admin-login
Content-Type: application/x-www-form-urlencoded
Parameters: username, password
Response: Redirect to admin dashboard

# Export Data
GET /export-candidate-shortlist
Response: CSV file download

# Advanced Filtering
POST /advanced-shortlist
Content-Type: application/x-www-form-urlencoded
Parameters: filter criteria
Response: Filtered candidate list
```

#### 5.1.3 Analytics APIs
```python
# Resume Statistics
GET /resume-statistics
Response: Statistical dashboard

# Generate Report
POST /generate-report
Content-Type: application/json
Parameters: candidate data
Response: PDF report download
```

### 5.2 API Response Formats

#### 5.2.1 Success Response
```json
{
  "success": true,
  "data": {
    "parsed_data": {...},
    "ats_score": 85,
    "improvements": [...],
    "recommendations": [...]
  }
}
```

#### 5.2.2 Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

---

## 6. Security Design

### 6.1 Authentication and Authorization

#### 6.1.1 User Authentication
```python
# Password Hashing (Recommended Implementation)
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

#### 6.1.2 Session Management
```python
# Secure Session Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
```

#### 6.1.3 Role-based Access Control
```python
# Admin Access Control
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
```

### 6.2 Data Security

#### 6.2.1 File Upload Security
```python
# File Validation
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

#### 6.2.2 SQL Injection Prevention
```python
# SQLAlchemy ORM prevents SQL injection
# Parameterized queries
candidate = sqlalchemy_session.query(CandidateProfile).filter_by(
    email=email
).first()
```

#### 6.2.3 XSS Prevention
```python
# Input Sanitization
from markupsafe import escape

def sanitize_input(user_input):
    return escape(user_input)
```

### 6.3 API Security

#### 6.3.1 Rate Limiting
```python
# Basic Rate Limiting (Recommended Implementation)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

#### 6.3.2 CORS Configuration
```python
# CORS Headers
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 7. Performance Considerations

### 7.1 Database Optimization

#### 7.1.1 Indexing Strategy
```sql
-- Primary Indexes
PRIMARY KEY (id)

-- Secondary Indexes
INDEX idx_candidate_email (email)
INDEX idx_candidate_ats_score (ats_score)
INDEX idx_candidate_uploaded_at (uploaded_at)
INDEX idx_candidate_city (city)
INDEX idx_candidate_region (region)

-- Composite Indexes
INDEX idx_candidate_location (city, region)
INDEX idx_candidate_score_date (ats_score, uploaded_at)
```

#### 7.1.2 Query Optimization
```python
# Efficient Query Patterns
# Use specific column selection
candidates = sqlalchemy_session.query(
    CandidateProfile.id,
    CandidateProfile.name,
    CandidateProfile.email,
    CandidateProfile.ats_score
).filter(CandidateProfile.ats_score >= 50).all()

# Use pagination for large datasets
candidates = sqlalchemy_session.query(CandidateProfile).offset(
    page * per_page
).limit(per_page).all()
```

### 7.2 File Processing Optimization

#### 7.2.1 Asynchronous Processing
```python
# Background Task Processing (Recommended Implementation)
from celery import Celery

celery = Celery('cvisionary', broker='redis://localhost:6379/0')

@celery.task
def process_resume_async(file_path):
    # Process resume in background
    # Update database when complete
    pass
```

#### 7.2.2 File Size Management
```python
# File Size Validation
def validate_file_size(file):
    if file.content_length > MAX_FILE_SIZE:
        raise ValueError("File too large")
    return True
```

### 7.3 AI Processing Optimization

#### 7.3.1 Request Batching
```python
# Batch AI Requests
def batch_process_resumes(resume_list):
    # Process multiple resumes in single AI request
    # Reduce API calls
    pass
```

#### 7.3.2 Response Caching
```python
# Cache AI Responses (Recommended Implementation)
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_ai_response(key):
    return redis_client.get(key)

def cache_ai_response(key, response):
    redis_client.setex(key, 3600, response)  # 1 hour expiry
```

---

## 8. Scalability Strategy

### 8.1 Horizontal Scaling

#### 8.1.1 Load Balancer Configuration
```nginx
# Nginx Load Balancer Configuration
upstream cvisionary_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name cvisionary.com;
    
    location / {
        proxy_pass http://cvisionary_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 8.1.2 Database Scaling
```sql
-- Read Replicas for Analytics
-- Master database for writes
-- Read replicas for reporting and analytics

-- Database Partitioning
ALTER TABLE candidate_profiles
PARTITION BY RANGE (YEAR(uploaded_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 8.2 Vertical Scaling

#### 8.2.1 Resource Optimization
```python
# Memory Management
import gc

def cleanup_memory():
    gc.collect()

# Connection Pooling
engine = create_engine(
    "mysql://user:pass@localhost/db",
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600
)
```

#### 8.2.2 Process Management
```python
# Multi-process Configuration
if __name__ == '__main__':
    from multiprocessing import Process
    
    def run_server(port):
        app.run(host='0.0.0.0', port=port)
    
    processes = []
    for port in [5000, 5001, 5002]:
        p = Process(target=run_server, args=(port,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
```

---

## 9. Error Handling

### 9.1 Application Error Handling

#### 9.1.1 Global Error Handlers
```python
# Global Exception Handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    sqlalchemy_session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    app.logger.error(f"Unhandled exception: {str(e)}")
    return render_template('error.html'), 500
```

#### 9.1.2 File Processing Error Handling
```python
def safe_file_processing(file_path):
    try:
        result = process_file(file_path)
        return result
    except FileNotFoundError:
        return {"error": "File not found"}
    except PermissionError:
        return {"error": "Permission denied"}
    except Exception as e:
        app.logger.error(f"File processing error: {str(e)}")
        return {"error": "Processing failed"}
```

### 9.2 Database Error Handling

#### 9.2.1 Connection Error Handling
```python
def safe_database_operation(operation):
    try:
        result = operation()
        sqlalchemy_session.commit()
        return result
    except Exception as e:
        sqlalchemy_session.rollback()
        app.logger.error(f"Database error: {str(e)}")
        raise
```

#### 9.2.2 Data Validation
```python
def validate_candidate_data(data):
    errors = []
    
    if not data.get('email'):
        errors.append("Email is required")
    
    if not data.get('name'):
        errors.append("Name is required")
    
    if data.get('ats_score') and not (0 <= data['ats_score'] <= 100):
        errors.append("ATS score must be between 0 and 100")
    
    return errors
```

### 9.3 AI Processing Error Handling

#### 9.3.1 API Error Handling
```python
def safe_ai_processing(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        app.logger.error(f"AI processing error: {str(e)}")
        return None
```

#### 9.3.2 Response Validation
```python
def validate_ai_response(response):
    try:
        parsed = json.loads(response)
        required_fields = ['name', 'email', 'skills']
        
        for field in required_fields:
            if field not in parsed:
                return False
        
        return True
    except json.JSONDecodeError:
        return False
```

---

## 10. Monitoring and Logging

### 10.1 Application Logging

#### 10.1.1 Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/cvisionary.log', 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('CVisionary startup')
```

#### 10.1.2 Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        app.logger.info(f"{f.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return decorated_function
```

### 10.2 Database Monitoring

#### 10.2.1 Query Performance Monitoring
```python
def log_slow_queries(query, execution_time):
    if execution_time > 1.0:  # Log queries taking more than 1 second
        app.logger.warning(f"Slow query detected: {query} took {execution_time}s")
```

#### 10.2.2 Connection Pool Monitoring
```python
def monitor_connection_pool():
    pool = engine.pool
    app.logger.info(f"Connection pool status: {pool.size()}/{pool.checkedin()}")
```

### 10.3 System Health Checks

#### 10.3.1 Health Check Endpoint
```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        sqlalchemy_session.execute("SELECT 1")
        
        # Check file system
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "filesystem": "accessible",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
```

---

## 11. Deployment Strategy

### 11.1 Development Environment

#### 11.1.1 Local Development Setup
```bash
# Virtual Environment Setup
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Environment Variables
export FLASK_APP=app.py
export FLASK_ENV=development
export GOOGLE_API_KEY=your_api_key

# Run Development Server
python app.py
```

#### 11.1.2 Development Configuration
```python
# Development Configuration
class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-secret-key'
    DATABASE_URL = 'mysql://root:root10@localhost/resume_analysis'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
```

### 11.2 Production Environment

#### 11.2.1 Production Server Setup
```python
# Production Configuration
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    UPLOAD_FOLDER = '/var/www/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
```

#### 11.2.2 WSGI Server Configuration
```python
# WSGI Application
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

#### 11.2.3 Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

### 11.3 Environment Management

#### 11.3.1 Environment Variables
```bash
# .env file
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
GOOGLE_API_KEY=your-gemini-api-key
DATABASE_URL=mysql://user:pass@host/database
UPLOAD_FOLDER=/var/www/uploads
MAX_CONTENT_LENGTH=16777216
```

#### 11.3.2 Configuration Management
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql://YourUsername:password@localhost/resume_analysis'
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
```

---

## 12. Appendices

### 12.1 File Structure
```
CVisionary/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
├── SRS_Document.md      # Software Requirements Specification
├── Database_Schema_Design.md  # Database design
├── System_Design.md     # This document
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Image assets
├── templates/           # HTML templates
├── uploads/            # File upload directory
├── logs/               # Application logs
└── instance/           # Database files
```

### 12.2 Configuration Files

#### 12.2.1 requirements.txt
```
flask==2.0.1
python-dotenv==0.19.0
pdf2image==1.16.0
pytesseract==0.3.8
python-docx==0.8.11
PyPDF2==2.10.5
spacy==3.5.3
nltk==3.8.1
scikit-learn==1.2.2
pandas==1.5.3
numpy==1.23.5
Pillow==9.5.0
pdfminer.six==20221105
python-magic==0.4.27
google-generativeai==0.3.2
SQLAlchemy==2.0.25
mysqlclient==2.2.1
```

#### 12.2.2 .env Template
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GOOGLE_API_KEY=your-gemini-api-key
DATABASE_URL=mysql://root:root10@localhost/resume_analysis
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### 12.3 Performance Benchmarks

#### 12.3.1 Response Time Targets
- **Page Load**: < 3 seconds
- **File Upload**: < 30 seconds
- **AI Processing**: < 15 seconds
- **Database Queries**: < 1 second

#### 12.3.2 Throughput Targets
- **Concurrent Users**: 100+
- **Resume Processing**: 50/hour
- **Database Operations**: 1000/minute
- **File Uploads**: 100/hour

---

**Document Version:** 1.0  
**Last Updated:** August 2025  
**Approved By:** Development Team  
**Next Review:** September 2025
