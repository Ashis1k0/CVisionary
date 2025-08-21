# CVisionary - AI-Powered Resume Analysis System

![CVisionary Logo](static/images/upload-icon.svg)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

CVisionary is an intelligent resume analysis system that leverages Google's Gemini AI to automatically parse, analyze, and evaluate resumes. The system provides comprehensive ATS (Applicant Tracking System) scoring, job recommendations, and candidate management features for HR professionals and recruiters.

### Key Capabilities
- **AI-Powered Resume Parsing**: Extracts information from PDF and DOCX resumes using Google Gemini AI
- **ATS Scoring**: Calculates compatibility scores for Applicant Tracking Systems
- **Job Recommendations**: Suggests relevant job opportunities based on candidate skills
- **Candidate Management**: Advanced filtering and shortlisting capabilities
- **Data Export**: Export candidate data in CSV format
- **Analytics Dashboard**: Statistical insights on candidate demographics and skills

## ✨ Features

### 🔍 Resume Analysis
- **Multi-format Support**: PDF and DOCX file processing
- **Intelligent Text Extraction**: OCR capabilities for scanned documents
- **Structured Data Extraction**: 
  - Personal information (name, email, phone)
  - Technical skills and competencies
  - Education history and academic performance
  - Work experience and project details
  - Location and contact information

### 📊 ATS Optimization
- **Compatibility Scoring**: 0-100 ATS score calculation
- **Keyword Analysis**: Identifies relevant industry keywords
- **Format Optimization**: Ensures ATS-friendly resume structure
- **Improvement Suggestions**: AI-generated recommendations for enhancement

### 🎯 Job Matching
- **Skill-based Recommendations**: Matches candidate skills to job opportunities
- **Market Analysis**: Considers current job market trends
- **Match Percentage**: Provides compatibility scores for each recommendation
- **Skill Gap Analysis**: Identifies additional skills needed for target roles

### 👥 Candidate Management
- **Advanced Filtering**: Filter by ATS score, CGPA, graduation year, skills
- **Shortlisting**: Automatic shortlisting of high-scoring candidates
- **Search Functionality**: Name, phone, and skill-based search
- **Bulk Operations**: Export filtered candidate lists

### 📈 Analytics & Reporting
- **Statistical Dashboard**: Geographic and demographic insights
- **Skill Analytics**: Most common skills and competencies
- **Education Trends**: Degree and institution analysis
- **PDF Reports**: Generate detailed analysis reports

### 🔐 User Management
- **Admin Panel**: Secure admin interface for HR professionals
- **User Registration**: Candidate self-registration system
- **Session Management**: Secure login/logout functionality
- **Role-based Access**: Different permissions for admins and users

## 🛠 Technology Stack

### Backend
- **Python 3.11+**: Core programming language
- **Flask 2.0.1**: Web framework
- **SQLAlchemy 2.0.25**: ORM for database operations
- **MySQL**: Primary database system

### AI & ML
- **Google Gemini AI**: Natural language processing and analysis
- **Pytesseract**: OCR for image-based text extraction
- **NLTK 3.8.1**: Natural language processing
- **Scikit-learn 1.2.2**: Machine learning algorithms

### Document Processing
- **PyPDF2 2.10.5**: PDF text extraction
- **python-docx 0.8.11**: DOCX file processing
- **pdf2image 1.16.0**: PDF to image conversion
- **Pillow 9.5.0**: Image processing
- **pdfminer.six**: Advanced PDF text extraction

### Data Processing
- **Pandas 1.5.3**: Data manipulation and analysis
- **NumPy 1.23.5**: Numerical computing
- **ReportLab**: PDF report generation

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive user interface
- **Bootstrap**: UI framework for styling

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- MySQL Server 8.0+
- Tesseract OCR (for image processing)
- Google Cloud account with Gemini API access

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/CVisionary.git
cd CVisionary
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE resume_analysis;
```

2. Update database configuration in `app.py`:
```python
engine = create_engine("mysql://username:password@localhost/resume_analysis")
```

### Step 5: Environment Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cvisionary_db
DB_HOST=localhost
```

### Step 6: Initialize Database
```bash
python app.py
```

## ⚙️ Configuration

### Database Configuration
Update the database connection in `app.py`:
```python
# MySQL Database Configuration
db = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='resume_analysis'
)
```

### File Upload Settings
Configure upload settings in `app.py`:
```python
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### Admin Credentials
Default admin credentials (change in production):
- Username: `admin`
- Password: `admin123`

## 📖 Usage

### Starting the Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

### User Workflows

#### For Candidates
1. **Upload Resume**: Navigate to the home page and upload your resume (PDF/DOCX)
2. **View Analysis**: Review the extracted information and ATS score
3. **Get Recommendations**: View AI-generated job recommendations
4. **Download Report**: Generate and download a detailed PDF report

#### For HR Professionals
1. **Admin Login**: Access the admin panel with credentials
2. **View All Candidates**: Browse uploaded resumes in the admin dashboard
3. **Advanced Filtering**: Use filters to find specific candidates
4. **Export Data**: Download candidate lists in CSV format
5. **Analytics**: View statistical insights and trends

### Key Features Usage

#### Resume Upload
- Supported formats: PDF, DOCX
- Maximum file size: 16MB
- Automatic text extraction and parsing
- Real-time ATS score calculation

#### Advanced Shortlisting
- Filter by ATS score (minimum threshold)
- Filter by academic performance (CGPA, percentage)
- Filter by graduation year
- Filter by specific skills
- Export filtered results

#### Analytics Dashboard
- Geographic distribution of candidates
- Most common skills and competencies
- Education trends and degree analysis
- Regional candidate statistics

## 🔌 API Documentation

### Resume Upload Endpoint
```http
POST /upload
Content-Type: multipart/form-data

Parameters:
- resume: File (PDF/DOCX)

Response:
{
  "success": true,
  "parsed_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-123-456-7890",
    "skills": ["Python", "Machine Learning"],
    "education": [...],
    "experience": [...],
    "projects": [...]
  },
  "ats_score": 85,
  "improvements": [...]
}
```

### Job Recommendations Endpoint
```http
POST /job-recommendations
Content-Type: application/json

Request:
{
  "skills": ["Python", "Machine Learning", "SQL"]
}

Response:
{
  "recommendations": [
    {
      "title": "Data Scientist",
      "match_percentage": 85,
      "matching_skills": ["Python", "Machine Learning"],
      "recommended_skills": ["TensorFlow", "PyTorch"],
      "description": "Develop ML models..."
    }
  ]
}
```

### ATS Score Calculation
```http
POST /ats-score
Content-Type: application/json

Request:
{
  "parsed_data": {...}
}

Response:
{
  "score": 85
}
```

## 🗄️ Database Schema

### CandidateProfile Table
```sql
CREATE TABLE candidate_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    resume TEXT,
    skills TEXT,
    phone VARCHAR(20),
    education TEXT,
    experience TEXT,
    projects TEXT,
    ats_score INT,
    uploaded_at VARCHAR(50),
    city VARCHAR(100),
    region VARCHAR(100),
    cgpa VARCHAR(10),
    academic_percentage VARCHAR(10),
    graduation_year VARCHAR(10)
);
```

### Admin Table
```sql
CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
```

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Development

### Project Structure
```
CVisionary/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
├── templates/            # HTML templates
├── uploads/             # File upload directory
└── instance/            # Database files
```

### Adding New Features
1. **Backend**: Add routes in `app.py`
2. **Frontend**: Create templates in `templates/`
3. **Styling**: Update CSS in `static/css/`
4. **Database**: Update models and run migrations

### Testing
```bash
# Run the application in debug mode
python app.py

# Test file upload functionality
# Test admin panel access
# Test candidate filtering
```
## 👥 Team

| Name | GitHub |
|------|--------|
| Ashis Moharana | [@Ashis1k0](https://github.com/Ashis1k0) |
| Ashirbad Mohanty | [@ASHIRBAD07](https://github.com/ASHIRBAD07) |
| Aryan Devdarshi | [@aryandevdarshi-debug](https://github.com/aryandevdarshi-debug) |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add comments for complex functions
- Update documentation for new features
- Test thoroughly before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing capabilities
- Flask community for the excellent web framework
- Open source contributors for various Python libraries
- OCR community for text extraction tools

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for common solutions

---

**CVisionary** - Transforming resume analysis with AI intelligence 🚀 
