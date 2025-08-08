# Software Requirements Specification (SRS)
## CVisionary - AI-Powered Resume Analysis System

**Version:** 1.0  
**Date:** August 2025  
**Project:** CVisionary  
**Document Type:** Software Requirements Specification

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [Use Cases](#5-use-cases)
6. [System Architecture](#6-system-architecture)
7. [Data Requirements](#7-data-requirements)
8. [Interface Requirements](#8-interface-requirements)
9. [Performance Requirements](#9-performance-requirements)
10. [Security Requirements](#10-security-requirements)
11. [Constraints and Limitations](#11-constraints-and-limitations)

---

## 1. Introduction

### 1.1 Purpose
This document provides a comprehensive specification of the requirements for CVisionary, an AI-powered resume analysis system that leverages Google's Gemini AI to parse, analyze, and evaluate resumes for HR professionals and recruiters.

### 1.2 Scope
CVisionary is a web-based application that provides:
- Automated resume parsing and data extraction
- ATS (Applicant Tracking System) compatibility scoring
- AI-powered job recommendations
- Advanced candidate management and filtering
- Statistical analytics and reporting
- Secure user authentication and authorization

### 1.3 Definitions and Acronyms
- **ATS**: Applicant Tracking System
- **AI**: Artificial Intelligence
- **API**: Application Programming Interface
- **OCR**: Optical Character Recognition
- **HR**: Human Resources
- **CGPA**: Cumulative Grade Point Average
- **PDF**: Portable Document Format
- **DOCX**: Microsoft Word Document Format

### 1.4 References
- Google Gemini AI API Documentation
- Flask Web Framework Documentation
- MySQL Database Documentation
- SQLAlchemy ORM Documentation

---

## 2. System Overview

### 2.1 System Purpose
CVisionary aims to streamline the recruitment process by providing intelligent resume analysis, automated candidate evaluation, and data-driven insights for HR professionals.

### 2.2 System Context
The system serves two primary user groups:
1. **Candidates**: Job seekers uploading resumes for analysis
2. **HR Professionals**: Recruiters and HR managers managing candidate data

### 2.3 System Features
- Resume upload and parsing
- AI-powered data extraction
- ATS compatibility scoring
- Job recommendation engine
- Candidate management dashboard
- Advanced filtering and search
- Data export capabilities
- Statistical analytics

---

## 3. Functional Requirements

### 3.1 User Management

#### 3.1.1 User Registration
- **FR-1.1**: System shall allow candidates to register with username, email, and password
- **FR-1.2**: System shall validate email format and uniqueness
- **FR-1.3**: System shall enforce password strength requirements
- **FR-1.4**: System shall prevent duplicate username registration

#### 3.1.2 User Authentication
- **FR-1.5**: System shall provide login functionality for registered users
- **FR-1.6**: System shall provide admin login with secure credentials
- **FR-1.7**: System shall maintain user sessions securely
- **FR-1.8**: System shall provide logout functionality

#### 3.1.3 Role-Based Access
- **FR-1.9**: System shall provide different access levels for candidates and admins
- **FR-1.10**: System shall restrict admin functions to authorized users only

### 3.2 Resume Processing

#### 3.2.1 File Upload
- **FR-2.1**: System shall accept PDF and DOCX file formats
- **FR-2.2**: System shall validate file size (maximum 16MB)
- **FR-2.3**: System shall secure uploaded files
- **FR-2.4**: System shall handle file upload errors gracefully

#### 3.2.2 Text Extraction
- **FR-2.5**: System shall extract text from PDF files using PyPDF2
- **FR-2.6**: System shall extract text from DOCX files using python-docx
- **FR-2.7**: System shall use OCR for scanned documents when text extraction fails
- **FR-2.8**: System shall handle extraction errors and provide meaningful feedback

#### 3.2.3 AI-Powered Parsing
- **FR-2.9**: System shall use Google Gemini AI for intelligent data extraction
- **FR-2.10**: System shall extract personal information (name, email, phone)
- **FR-2.11**: System shall extract technical skills and competencies
- **FR-2.12**: System shall extract education history and academic performance
- **FR-2.13**: System shall extract work experience and project details
- **FR-2.14**: System shall extract location information

### 3.3 ATS Scoring

#### 3.3.1 Score Calculation
- **FR-3.1**: System shall calculate ATS compatibility scores (0-100)
- **FR-3.2**: System shall evaluate basic information completeness (20%)
- **FR-3.3**: System shall evaluate skills relevance and quantity (30%)
- **FR-3.4**: System shall evaluate education background (20%)
- **FR-3.5**: System shall evaluate work experience (30%)

#### 3.3.2 Score Components
- **FR-3.6**: System shall score name, email, and phone presence
- **FR-3.7**: System shall score skills based on quantity and relevance
- **FR-3.8**: System shall score education entries
- **FR-3.9**: System shall score experience entries

### 3.4 Job Recommendations

#### 3.4.1 Recommendation Generation
- **FR-4.1**: System shall generate job recommendations based on candidate skills
- **FR-4.2**: System shall provide match percentages for each recommendation
- **FR-4.3**: System shall identify matching skills for each job
- **FR-4.4**: System shall suggest additional skills needed for target roles
- **FR-4.5**: System shall provide job descriptions and requirements

#### 3.4.2 Market Analysis
- **FR-4.6**: System shall consider current job market trends
- **FR-4.7**: System shall provide realistic match percentages
- **FR-4.8**: System shall suggest complementary skills for each role

### 3.5 Candidate Management

#### 3.5.1 Data Storage
- **FR-5.1**: System shall store parsed resume data in MySQL database
- **FR-5.2**: System shall maintain data integrity and relationships
- **FR-5.3**: System shall handle data updates and modifications
- **FR-5.4**: System shall provide data backup and recovery

#### 3.5.2 Candidate Search
- **FR-5.5**: System shall allow searching by name, phone, and skills
- **FR-5.6**: System shall provide advanced filtering options
- **FR-5.7**: System shall support multiple search criteria simultaneously

#### 3.5.3 Shortlisting
- **FR-5.8**: System shall automatically shortlist candidates with ATS score ≥ 50
- **FR-5.9**: System shall provide manual shortlisting capabilities
- **FR-5.10**: System shall allow custom shortlisting criteria

### 3.6 Advanced Filtering

#### 3.6.1 Filter Criteria
- **FR-6.1**: System shall filter by minimum ATS score
- **FR-6.2**: System shall filter by minimum CGPA
- **FR-6.3**: System shall filter by minimum academic percentage
- **FR-6.4**: System shall filter by graduation year
- **FR-6.5**: System shall filter by specific skills

#### 3.6.2 Filter Operations
- **FR-6.6**: System shall support multiple filter criteria simultaneously
- **FR-6.7**: System shall provide real-time filter results
- **FR-6.8**: System shall save filter configurations

### 3.7 Data Export

#### 3.7.1 Export Formats
- **FR-7.1**: System shall export data in CSV format
- **FR-7.2**: System shall export filtered candidate lists
- **FR-7.3**: System shall export shortlisted candidates
- **FR-7.4**: System shall include all relevant candidate information in exports

#### 3.7.2 Export Features
- **FR-7.5**: System shall generate timestamped export files
- **FR-7.6**: System shall provide download links for exported files
- **FR-7.7**: System shall handle export errors gracefully

### 3.8 Analytics and Reporting

#### 3.8.1 Statistical Dashboard
- **FR-8.1**: System shall provide geographic distribution statistics
- **FR-8.2**: System shall provide skill frequency analysis
- **FR-8.3**: System shall provide education trend analysis
- **FR-8.4**: System shall provide regional candidate statistics

#### 3.8.2 Report Generation
- **FR-8.5**: System shall generate PDF reports for individual candidates
- **FR-8.6**: System shall include ATS scores in reports
- **FR-8.7**: System shall include improvement suggestions in reports
- **FR-8.8**: System shall include job recommendations in reports

### 3.9 Resume Improvements

#### 3.9.1 Improvement Suggestions
- **FR-9.1**: System shall generate specific improvement suggestions
- **FR-9.2**: System shall focus on ATS optimization
- **FR-9.3**: System shall provide actionable recommendations
- **FR-9.4**: System shall tailor suggestions to individual resumes

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

#### 4.1.1 Response Time
- **NFR-1.1**: System shall respond to user requests within 3 seconds
- **NFR-1.2**: Resume upload and processing shall complete within 30 seconds
- **NFR-1.3**: Database queries shall execute within 1 second
- **NFR-1.4**: AI processing shall complete within 15 seconds

#### 4.1.2 Throughput
- **NFR-1.5**: System shall handle 100 concurrent users
- **NFR-1.6**: System shall process 50 resume uploads per hour
- **NFR-1.7**: System shall support 1000 database operations per minute

#### 4.1.3 Scalability
- **NFR-1.8**: System shall scale horizontally with additional servers
- **NFR-1.9**: Database shall support up to 10,000 candidate records
- **NFR-1.10**: System shall handle increasing load without performance degradation

### 4.2 Reliability Requirements

#### 4.2.1 Availability
- **NFR-2.1**: System shall be available 99.5% of the time
- **NFR-2.2**: System shall provide graceful error handling
- **NFR-2.3**: System shall recover from failures automatically

#### 4.2.2 Data Integrity
- **NFR-2.4**: System shall maintain data consistency
- **NFR-2.5**: System shall prevent data corruption
- **NFR-2.6**: System shall provide data backup and recovery

### 4.3 Security Requirements

#### 4.3.1 Authentication
- **NFR-3.1**: System shall use secure password hashing
- **NFR-3.2**: System shall implement session management
- **NFR-3.3**: System shall prevent unauthorized access

#### 4.3.2 Data Protection
- **NFR-3.4**: System shall encrypt sensitive data
- **NFR-3.5**: System shall protect user privacy
- **NFR-3.6**: System shall comply with data protection regulations

#### 4.3.3 File Security
- **NFR-3.7**: System shall validate uploaded files
- **NFR-3.8**: System shall prevent file-based attacks
- **NFR-3.9**: System shall secure file storage

### 4.4 Usability Requirements

#### 4.4.1 User Interface
- **NFR-4.1**: System shall provide intuitive user interface
- **NFR-4.2**: System shall be responsive across different devices
- **NFR-4.3**: System shall provide clear error messages
- **NFR-4.4**: System shall provide helpful user guidance

#### 4.4.2 Accessibility
- **NFR-4.5**: System shall be accessible to users with disabilities
- **NFR-4.6**: System shall support screen readers
- **NFR-4.7**: System shall provide keyboard navigation

### 4.5 Compatibility Requirements

#### 4.5.1 Browser Support
- **NFR-5.1**: System shall work on Chrome, Firefox, Safari, and Edge
- **NFR-5.2**: System shall support mobile browsers
- **NFR-5.3**: System shall be responsive on different screen sizes

#### 4.5.2 File Format Support
- **NFR-5.4**: System shall support PDF files (version 1.4 and above)
- **NFR-5.5**: System shall support DOCX files (Office 2007 and above)
- **NFR-5.6**: System shall handle various PDF and DOCX formats

### 4.6 Maintainability Requirements

#### 4.6.1 Code Quality
- **NFR-6.1**: System shall follow coding standards
- **NFR-6.2**: System shall be well-documented
- **NFR-6.3**: System shall be modular and extensible

#### 4.6.2 Testing
- **NFR-6.4**: System shall have comprehensive test coverage
- **NFR-6.5**: System shall support automated testing
- **NFR-6.6**: System shall provide testing documentation

---

## 5. Use Cases

### 5.1 Candidate Use Cases

#### UC-1: Resume Upload and Analysis
**Actor:** Candidate  
**Precondition:** Candidate has registered account  
**Main Flow:**
1. Candidate logs into the system
2. Candidate uploads resume (PDF/DOCX)
3. System processes and extracts data
4. System calculates ATS score
5. System generates job recommendations
6. System provides improvement suggestions
7. Candidate views analysis results

**Alternative Flow:**
- If file format is invalid, system shows error message
- If processing fails, system provides retry option

#### UC-2: Job Recommendations
**Actor:** Candidate  
**Precondition:** Candidate has uploaded resume  
**Main Flow:**
1. Candidate requests job recommendations
2. System analyzes candidate skills
3. System generates relevant job matches
4. System provides match percentages
5. System suggests additional skills needed
6. Candidate views recommendations

### 5.2 Admin Use Cases

#### UC-3: Candidate Management
**Actor:** Admin  
**Precondition:** Admin is logged in  
**Main Flow:**
1. Admin accesses candidate dashboard
2. Admin views all uploaded resumes
3. Admin filters candidates by criteria
4. Admin shortlists candidates
5. Admin exports candidate data
6. Admin manages candidate records

#### UC-4: Advanced Filtering
**Actor:** Admin  
**Precondition:** Admin is logged in  
**Main Flow:**
1. Admin accesses advanced filtering
2. Admin sets filter criteria (ATS score, CGPA, skills)
3. System applies filters
4. System displays filtered results
5. Admin exports filtered data
6. Admin saves filter configuration

#### UC-5: Analytics Dashboard
**Actor:** Admin  
**Precondition:** Admin is logged in  
**Main Flow:**
1. Admin accesses analytics dashboard
2. System displays statistical insights
3. Admin views geographic distribution
4. Admin views skill analytics
5. Admin views education trends
6. Admin generates reports

---

## 6. System Architecture

### 6.1 High-Level Architecture
The system follows a three-tier architecture:
1. **Presentation Layer**: Web interface (HTML, CSS, JavaScript)
2. **Application Layer**: Flask web application with business logic
3. **Data Layer**: MySQL database with SQLAlchemy ORM

### 6.2 Technology Stack
- **Backend**: Python, Flask, SQLAlchemy
- **Database**: MySQL
- **AI/ML**: Google Gemini AI, NLTK, Scikit-learn
- **Document Processing**: PyPDF2, python-docx, pytesseract
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap

### 6.3 Component Architecture
- **Web Server**: Flask application
- **AI Engine**: Google Gemini AI integration
- **Document Processor**: Multi-format text extraction
- **Database Engine**: MySQL with SQLAlchemy
- **File Storage**: Local file system
- **Session Management**: Flask sessions

---

## 7. Data Requirements

### 7.1 Data Types
- **User Data**: Authentication and profile information
- **Resume Data**: Parsed resume information
- **Analysis Data**: ATS scores and recommendations
- **Analytics Data**: Statistical and trend information

### 7.2 Data Volume
- **Expected Users**: 1,000+ candidates
- **Expected Resumes**: 5,000+ processed resumes
- **Database Size**: 1GB+ storage requirement
- **File Storage**: 10GB+ for uploaded files

### 7.3 Data Quality
- **Accuracy**: 95%+ data extraction accuracy
- **Completeness**: 90%+ field completion rate
- **Consistency**: Standardized data formats
- **Validity**: Data validation and sanitization

---

## 8. Interface Requirements

### 8.1 User Interfaces
- **Web Interface**: Responsive web application
- **Admin Dashboard**: Advanced management interface
- **Candidate Portal**: Simple upload and analysis interface
- **Analytics Dashboard**: Statistical visualization interface

### 8.2 External Interfaces
- **Google Gemini AI API**: AI processing and analysis
- **MySQL Database**: Data storage and retrieval
- **File System**: Document storage and management
- **Email System**: Notifications and alerts

### 8.3 API Interfaces
- **RESTful APIs**: For external integrations
- **Webhook Support**: For real-time notifications
- **Export APIs**: For data export functionality
- **Authentication APIs**: For secure access

---

## 9. Performance Requirements

### 9.1 Response Time
- **Page Load**: < 3 seconds
- **File Upload**: < 30 seconds
- **AI Processing**: < 15 seconds
- **Database Queries**: < 1 second

### 9.2 Throughput
- **Concurrent Users**: 100+
- **Resume Processing**: 50/hour
- **Database Operations**: 1000/minute
- **File Uploads**: 100/hour

### 9.3 Scalability
- **Horizontal Scaling**: Support for multiple servers
- **Database Scaling**: Support for read replicas
- **File Storage**: Support for cloud storage
- **Caching**: Redis for performance optimization

---

## 10. Security Requirements

### 10.1 Authentication
- **Password Security**: Bcrypt hashing
- **Session Management**: Secure session handling
- **Multi-factor Authentication**: Optional 2FA support
- **Password Policies**: Strong password requirements

### 10.2 Authorization
- **Role-based Access**: Different permissions for users and admins
- **Resource Protection**: Secure access to sensitive data
- **API Security**: Token-based authentication
- **File Access**: Secure file upload and download

### 10.3 Data Protection
- **Data Encryption**: AES encryption for sensitive data
- **Privacy Compliance**: GDPR and data protection compliance
- **Audit Logging**: Comprehensive activity logging
- **Data Backup**: Regular encrypted backups

---

## 11. Constraints and Limitations

### 11.1 Technical Constraints
- **File Size**: Maximum 16MB per upload
- **File Formats**: PDF and DOCX only
- **AI API Limits**: Google Gemini API rate limits
- **Database Limits**: MySQL connection limits

### 11.2 Business Constraints
- **Budget**: Limited development and hosting budget
- **Timeline**: 6-month development timeline
- **Team Size**: Small development team
- **Resources**: Limited computational resources

### 11.3 Regulatory Constraints
- **Data Privacy**: Compliance with data protection laws
- **AI Ethics**: Responsible AI usage guidelines
- **Accessibility**: WCAG 2.1 compliance
- **Security**: Industry security standards

---

## 12. Appendices

### 12.1 Glossary
- **ATS**: Applicant Tracking System - software used by employers to manage job applications
- **OCR**: Optical Character Recognition - technology to extract text from images
- **API**: Application Programming Interface - interface for software components
- **ORM**: Object-Relational Mapping - technique for database access

### 12.2 References
- Google Gemini AI Documentation
- Flask Web Framework Documentation
- MySQL Database Documentation
- SQLAlchemy ORM Documentation
- WCAG 2.1 Accessibility Guidelines

---

**Document Version:** 1.0  
**Last Updated:** August 2025  
**Approved By:** Development Team  
**Next Review:** September 2025 