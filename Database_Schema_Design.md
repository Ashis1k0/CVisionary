# Database Schema Design
## CVisionary - AI-Powered Resume Analysis System

**Version:** 1.0  
**Date:** January 2025  
**Project:** CVisionary  
**Document Type:** Database Schema Design

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Database Overview](#2-database-overview)
3. [Entity Relationship Diagram](#3-entity-relationship-diagram)
4. [Table Definitions](#4-table-definitions)
5. [Data Types and Constraints](#5-data-types-and-constraints)
6. [Indexes and Performance](#6-indexes-and-performance)
7. [Data Flow](#7-data-flow)
8. [Security Considerations](#8-security-considerations)
9. [Backup and Recovery](#9-backup-and-recovery)
10. [Migration Strategy](#10-migration-strategy)

---

## 1. Introduction

### 1.1 Purpose
This document provides a comprehensive database schema design for CVisionary, including table structures, relationships, constraints, and data management strategies.

### 1.2 Scope
The database design covers all data storage requirements for:
- User authentication and authorization
- Resume data storage and management
- AI analysis results and scores
- Candidate management and filtering
- Analytics and reporting data

### 1.3 Database Technology
- **Database Engine**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0.25
- **Connection**: mysqlclient 2.2.1
- **Character Set**: UTF-8
- **Collation**: utf8mb4_unicode_ci

---

## 2. Database Overview

### 2.1 Database Name
```sql
CREATE DATABASE resume_analysis
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 2.2 Database Connection
```python
# Connection String
mysql://root:root10@localhost/resume_analysis

# SQLAlchemy Engine Configuration
engine = create_engine(
    "mysql://username:password@localhost/resume_analysis",
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)
```

### 2.3 Database Statistics
- **Total Tables**: 3 main tables
- **Estimated Size**: 1GB+ for 10,000 candidates
- **Backup Frequency**: Daily automated backups
- **Retention Policy**: 30 days for backups

---

## 3. Entity Relationship Diagram

### 3.1 High-Level ERD
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│      Admin      │    │       User       │    │  CandidateProfile   │
├─────────────────┤    ├──────────────────┤    ├─────────────────────┤
│ id (PK)         │    │ id (PK)          │    │ id (PK)             │
│ username (UK)   │    │ username (UK)    │    │ email (UK)          │
│ password        │    │ email (UK)       │    │ name                │
└─────────────────┘    │ password         │    │ resume              │
                       │ created_at       │    │ skills              │
                       └──────────────────┘    │ phone               │
                                               │ education           │
                                               │ experience          │
                                               │ projects            │
                                               │ ats_score           │
                                               │ uploaded_at         │
                                               │ city                │
                                               │ region              │
                                               │ cgpa                │
                                               │ academic_percentage │
                                               │ graduation_year     │
                                               └─────────────────────┘
```

### 3.2 Relationships
- **Admin** ↔ **User**: No direct relationship (separate authentication systems)
- **User** ↔ **CandidateProfile**: One-to-many (one user can have multiple profiles)
- **Admin** ↔ **CandidateProfile**: Many-to-many (admins manage all profiles)

---

## 4. Table Definitions

### 4.1 Admin Table
```sql
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_admin_username (username),
    INDEX idx_admin_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Purpose**: Store admin user credentials for system administration.

**Key Features**:
- Unique username constraint
- Hashed password storage
- Audit timestamps
- Optimized indexing

### 4.2 Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_users_username (username),
    INDEX idx_users_email (email),
    INDEX idx_users_created_at (created_at),
    INDEX idx_users_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Purpose**: Store candidate user accounts for resume upload and analysis.

**Key Features**:
- Unique username and email constraints
- Account status tracking
- Login timestamp tracking
- Comprehensive indexing

### 4.3 CandidateProfile Table
```sql
CREATE TABLE candidate_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    resume TEXT,
    skills JSON,
    phone VARCHAR(20),
    education JSON,
    experience JSON,
    projects JSON,
    ats_score INT DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    city VARCHAR(100),
    region VARCHAR(100),
    cgpa VARCHAR(10),
    academic_percentage VARCHAR(10),
    graduation_year VARCHAR(10),
    is_shortlisted BOOLEAN DEFAULT FALSE,
    shortlisted_at TIMESTAMP NULL,
    shortlisted_by INT NULL,
    
    INDEX idx_candidate_email (email),
    INDEX idx_candidate_name (name),
    INDEX idx_candidate_ats_score (ats_score),
    INDEX idx_candidate_uploaded_at (uploaded_at),
    INDEX idx_candidate_city (city),
    INDEX idx_candidate_region (region),
    INDEX idx_candidate_shortlisted (is_shortlisted),
    INDEX idx_candidate_skills ((CAST(skills AS CHAR(1000)))),
    INDEX idx_candidate_education ((CAST(education AS CHAR(1000)))),
    INDEX idx_candidate_experience ((CAST(experience AS CHAR(1000)))),
    
    FOREIGN KEY (shortlisted_by) REFERENCES admin(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Purpose**: Store parsed resume data and analysis results for each candidate.

**Key Features**:
- JSON storage for complex data (skills, education, experience, projects)
- ATS score tracking
- Geographic information
- Academic performance metrics
- Shortlisting functionality
- Comprehensive indexing for search and filtering

---

## 5. Data Types and Constraints

### 5.1 Data Type Specifications

#### 5.1.1 String Fields
- **VARCHAR(50)**: Usernames, short identifiers
- **VARCHAR(100)**: Email addresses, city names
- **VARCHAR(255)**: Names, titles
- **VARCHAR(20)**: Phone numbers
- **VARCHAR(10)**: Academic scores, years
- **TEXT**: Resume content, long descriptions

#### 5.1.2 JSON Fields
- **skills**: Array of skill strings
- **education**: Array of education objects
- **experience**: Array of experience objects
- **projects**: Array of project objects

#### 5.1.3 Numeric Fields
- **INT**: IDs, scores, counts
- **BOOLEAN**: Status flags
- **TIMESTAMP**: Date and time tracking

### 5.2 Constraints

#### 5.2.1 Primary Keys
```sql
-- All tables use AUTO_INCREMENT INT primary keys
id INT AUTO_INCREMENT PRIMARY KEY
```

#### 5.2.2 Unique Constraints
```sql
-- Admin table
username VARCHAR(50) UNIQUE NOT NULL

-- Users table
username VARCHAR(50) UNIQUE NOT NULL
email VARCHAR(100) UNIQUE NOT NULL

-- CandidateProfile table
email VARCHAR(255) UNIQUE NOT NULL
```

#### 5.2.3 Foreign Key Constraints
```sql
-- CandidateProfile references Admin for shortlisting
FOREIGN KEY (shortlisted_by) REFERENCES admin(id) ON DELETE SET NULL
```

#### 5.2.4 Check Constraints
```sql
-- ATS Score range validation
CONSTRAINT chk_ats_score CHECK (ats_score >= 0 AND ats_score <= 100)

-- Email format validation
CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

-- Phone number format validation
CONSTRAINT chk_phone_format CHECK (phone REGEXP '^[+]?[0-9\s\-\(\)]{10,20}$')
```

### 5.3 Default Values
```sql
-- Timestamp defaults
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- Score defaults
ats_score INT DEFAULT 0

-- Status defaults
is_active BOOLEAN DEFAULT TRUE
is_shortlisted BOOLEAN DEFAULT FALSE
```

---

## 6. Indexes and Performance

### 6.1 Primary Indexes
```sql
-- Primary key indexes (automatic)
PRIMARY KEY (id)
```

### 6.2 Secondary Indexes
```sql
-- Admin table indexes
INDEX idx_admin_username (username)
INDEX idx_admin_created_at (created_at)

-- Users table indexes
INDEX idx_users_username (username)
INDEX idx_users_email (email)
INDEX idx_users_created_at (created_at)
INDEX idx_users_active (is_active)

-- CandidateProfile table indexes
INDEX idx_candidate_email (email)
INDEX idx_candidate_name (name)
INDEX idx_candidate_ats_score (ats_score)
INDEX idx_candidate_uploaded_at (uploaded_at)
INDEX idx_candidate_city (city)
INDEX idx_candidate_region (region)
INDEX idx_candidate_shortlisted (is_shortlisted)
```

### 6.3 JSON Indexes
```sql
-- JSON field indexes for search functionality
INDEX idx_candidate_skills ((CAST(skills AS CHAR(1000))))
INDEX idx_candidate_education ((CAST(education AS CHAR(1000))))
INDEX idx_candidate_experience ((CAST(experience AS CHAR(1000))))
```

### 6.4 Composite Indexes
```sql
-- Composite indexes for complex queries
INDEX idx_candidate_location (city, region)
INDEX idx_candidate_score_date (ats_score, uploaded_at)
INDEX idx_candidate_academic (cgpa, academic_percentage, graduation_year)
```

### 6.5 Performance Optimization

#### 6.5.1 Query Optimization
```sql
-- Example optimized queries
SELECT * FROM candidate_profiles 
WHERE ats_score >= 50 
AND uploaded_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY ats_score DESC, uploaded_at DESC;

SELECT city, COUNT(*) as candidate_count 
FROM candidate_profiles 
WHERE is_shortlisted = TRUE 
GROUP BY city 
ORDER BY candidate_count DESC;
```

#### 6.5.2 Partitioning Strategy
```sql
-- Partition by upload date for large datasets
ALTER TABLE candidate_profiles
PARTITION BY RANGE (YEAR(uploaded_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

---

## 7. Data Flow

### 7.1 Data Entry Flow
```
1. User Registration → users table
2. Resume Upload → File System + candidate_profiles table
3. AI Processing → candidate_profiles table (JSON fields)
4. ATS Scoring → candidate_profiles table (ats_score field)
5. Admin Actions → candidate_profiles table (shortlisting)
```

### 7.2 Data Retrieval Flow
```
1. User Login → users table (authentication)
2. Admin Login → admin table (authentication)
3. Candidate Search → candidate_profiles table (filtering)
4. Analytics → candidate_profiles table (aggregation)
5. Export → candidate_profiles table (CSV generation)
```

### 7.3 Data Update Flow
```
1. Profile Updates → candidate_profiles table (UPDATE)
2. Score Recalculation → candidate_profiles table (UPDATE)
3. Shortlisting → candidate_profiles table (UPDATE)
4. User Management → users table (UPDATE)
```

### 7.4 Data Backup Flow
```
1. Daily Backup → Full database backup
2. Incremental Backup → Changed data only
3. Archive Backup → Monthly full backups
4. Recovery → Point-in-time recovery
```

---

## 8. Security Considerations

### 8.1 Authentication Security
```sql
-- Password hashing (application level)
-- Use bcrypt or similar for password hashing
-- Never store plain text passwords

-- Session management
-- Secure session tokens
-- Session timeout configuration
```

### 8.2 Data Encryption
```sql
-- Column-level encryption for sensitive data
ALTER TABLE candidate_profiles 
MODIFY COLUMN phone VARBINARY(255);

-- File-level encryption for uploaded resumes
-- Encrypt files before storage
-- Decrypt files for processing
```

### 8.3 Access Control
```sql
-- Database user permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON resume_analysis.* TO 'app_user'@'localhost';
GRANT SELECT ON resume_analysis.* TO 'readonly_user'@'localhost';

-- Row-level security (application level)
-- Filter queries based on user permissions
-- Implement role-based access control
```

### 8.4 Audit Logging
```sql
-- Create audit table for tracking changes
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_values JSON,
    new_values JSON,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_audit_table_record (table_name, record_id),
    INDEX idx_audit_timestamp (timestamp),
    INDEX idx_audit_user (user_id)
);
```

---

## 9. Backup and Recovery

### 9.1 Backup Strategy
```bash
# Daily full backup
mysqldump --single-transaction --routines --triggers \
  --all-databases > backup_$(date +%Y%m%d).sql

# Incremental backup using binary logs
mysqlbinlog --start-datetime="2025-01-01 00:00:00" \
  --stop-datetime="2025-01-01 23:59:59" \
  mysql-bin.000001 > incremental_backup.sql
```

### 9.2 Recovery Procedures
```sql
-- Point-in-time recovery
RESTORE FROM backup_20250101.sql;
APPLY LOG incremental_backup.sql;

-- Table-level recovery
RESTORE TABLE candidate_profiles FROM backup_20250101.sql;

-- Data recovery procedures
-- Document step-by-step recovery process
-- Test recovery procedures regularly
```

### 9.3 Backup Retention
- **Daily Backups**: 7 days retention
- **Weekly Backups**: 4 weeks retention
- **Monthly Backups**: 12 months retention
- **Yearly Backups**: 5 years retention

---

## 10. Migration Strategy

### 10.1 Schema Evolution
```sql
-- Version 1.0 to 1.1 migration
ALTER TABLE candidate_profiles 
ADD COLUMN is_shortlisted BOOLEAN DEFAULT FALSE,
ADD COLUMN shortlisted_at TIMESTAMP NULL,
ADD COLUMN shortlisted_by INT NULL,
ADD FOREIGN KEY (shortlisted_by) REFERENCES admin(id);

-- Add new indexes
CREATE INDEX idx_candidate_shortlisted ON candidate_profiles(is_shortlisted);
```

### 10.2 Data Migration
```sql
-- Migrate existing data
UPDATE candidate_profiles 
SET is_shortlisted = TRUE 
WHERE ats_score >= 70;

-- Update data formats
UPDATE candidate_profiles 
SET skills = JSON_ARRAY(skills) 
WHERE skills IS NOT NULL AND skills NOT LIKE '[%]';
```

### 10.3 Rollback Strategy
```sql
-- Rollback procedures
-- Document rollback steps for each migration
-- Test rollback procedures before production deployment
-- Maintain backup before each migration
```

---

## 11. Monitoring and Maintenance

### 11.1 Performance Monitoring
```sql
-- Monitor query performance
SHOW PROCESSLIST;
EXPLAIN SELECT * FROM candidate_profiles WHERE ats_score >= 50;

-- Monitor table sizes
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'resume_analysis';
```

### 11.2 Maintenance Tasks
```sql
-- Regular maintenance procedures
OPTIMIZE TABLE candidate_profiles;
ANALYZE TABLE candidate_profiles;

-- Clean up old data
DELETE FROM candidate_profiles 
WHERE uploaded_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Update statistics
ANALYZE TABLE candidate_profiles;
```

### 11.3 Health Checks
```sql
-- Database health check queries
SELECT COUNT(*) as total_candidates FROM candidate_profiles;
SELECT COUNT(*) as shortlisted_candidates FROM candidate_profiles WHERE is_shortlisted = TRUE;
SELECT AVG(ats_score) as avg_ats_score FROM candidate_profiles;
```

---

## 12. Appendices

### 12.1 SQLAlchemy Models
```python
# Complete SQLAlchemy model definitions
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
    resume = Column(Text)
    skills = Column(Text)  # JSON string
    phone = Column(String(20))
    education = Column(Text)  # JSON string
    experience = Column(Text)  # JSON string
    projects = Column(Text)  # JSON string
    ats_score = Column(Integer, default=0)
    uploaded_at = Column(String(50))
    city = Column(String(100))
    region = Column(String(100))
    cgpa = Column(String(10))
    academic_percentage = Column(String(10))
    graduation_year = Column(String(10))
```

### 12.2 Sample Data
```sql
-- Sample admin user
INSERT INTO admin (username, password) VALUES ('admin', 'hashed_password');

-- Sample user
INSERT INTO users (username, email, password) 
VALUES ('john_doe', 'john@example.com', 'hashed_password');

-- Sample candidate profile
INSERT INTO candidate_profiles (
    email, name, skills, phone, ats_score, city, region
) VALUES (
    'john@example.com',
    'John Doe',
    '["Python", "Machine Learning", "SQL"]',
    '+1-123-456-7890',
    85,
    'San Francisco',
    'California'
);
```

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Approved By:** Development Team  
**Next Review:** March 2025 