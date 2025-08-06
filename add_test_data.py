import mysql.connector
import json
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root10',
    'database': 'resume_analysis'
}

def add_test_candidates():
    """Add test candidates with academic performance data"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Test candidates with academic data
        test_candidates = [
            {
                'name': 'Rahul Kumar',
                'email': 'rahul.kumar@test.com',
                'phone': '+91-9876543210',
                'skills': json.dumps(['Python', 'Java', 'SQL', 'React', 'Node.js']),
                'education': json.dumps([
                    {
                        'degree': 'B.Tech Computer Science',
                        'institution': 'IIT Delhi',
                        'year': '2024'
                    }
                ]),
                'experience': json.dumps([
                    {
                        'title': 'Software Engineer',
                        'company': 'Tech Corp',
                        'duration': '2 years'
                    }
                ]),
                'projects': json.dumps([
                    {
                        'title': 'E-commerce Platform',
                        'description': 'Full-stack web application',
                        'technologies': ['React', 'Node.js', 'MongoDB'],
                        'duration': '6 months'
                    }
                ]),
                'ats_score': 85,
                'cgpa': '8.5',
                'academic_percentage': '85',
                'graduation_year': '2024',
                'city': 'Delhi',
                'region': 'India'
            },
            {
                'name': 'Priya Sharma',
                'email': 'priya.sharma@test.com',
                'phone': '+91-9876543211',
                'skills': json.dumps(['JavaScript', 'Python', 'MongoDB', 'Express.js', 'AWS']),
                'education': json.dumps([
                    {
                        'degree': 'B.Tech Information Technology',
                        'institution': 'NIT Trichy',
                        'year': '2023'
                    }
                ]),
                'experience': json.dumps([
                    {
                        'title': 'Full Stack Developer',
                        'company': 'Startup Inc',
                        'duration': '1.5 years'
                    }
                ]),
                'projects': json.dumps([
                    {
                        'title': 'Task Management App',
                        'description': 'React-based task management system',
                        'technologies': ['React', 'Node.js', 'PostgreSQL'],
                        'duration': '4 months'
                    }
                ]),
                'ats_score': 78,
                'cgpa': '7.8',
                'academic_percentage': '78',
                'graduation_year': '2023',
                'city': 'Chennai',
                'region': 'India'
            },
            {
                'name': 'Amit Patel',
                'email': 'amit.patel@test.com',
                'phone': '+91-9876543212',
                'skills': json.dumps(['C++', 'Java', 'Data Structures', 'Algorithms', 'Linux']),
                'education': json.dumps([
                    {
                        'degree': 'B.Tech Computer Science',
                        'institution': 'BITS Pilani',
                        'year': '2025'
                    }
                ]),
                'experience': json.dumps([
                    {
                        'title': 'Software Developer',
                        'company': 'Tech Solutions',
                        'duration': '1 year'
                    }
                ]),
                'projects': json.dumps([
                    {
                        'title': 'Algorithm Visualizer',
                        'description': 'Interactive algorithm visualization tool',
                        'technologies': ['JavaScript', 'HTML5', 'CSS3'],
                        'duration': '3 months'
                    }
                ]),
                'ats_score': 92,
                'cgpa': '9.2',
                'academic_percentage': '92',
                'graduation_year': '2025',
                'city': 'Mumbai',
                'region': 'India'
            },
            {
                'name': 'Neha Singh',
                'email': 'neha.singh@test.com',
                'phone': '+91-9876543213',
                'skills': json.dumps(['Python', 'Machine Learning', 'TensorFlow', 'SQL', 'Git']),
                'education': json.dumps([
                    {
                        'degree': 'B.Tech Data Science',
                        'institution': 'IIIT Bangalore',
                        'year': '2024'
                    }
                ]),
                'experience': json.dumps([
                    {
                        'title': 'Data Scientist',
                        'company': 'AI Labs',
                        'duration': '2 years'
                    }
                ]),
                'projects': json.dumps([
                    {
                        'title': 'Sentiment Analysis Model',
                        'description': 'ML model for sentiment analysis',
                        'technologies': ['Python', 'TensorFlow', 'NLTK'],
                        'duration': '5 months'
                    }
                ]),
                'ats_score': 88,
                'cgpa': '8.8',
                'academic_percentage': '88',
                'graduation_year': '2024',
                'city': 'Bangalore',
                'region': 'India'
            },
            {
                'name': 'Vikram Malhotra',
                'email': 'vikram.malhotra@test.com',
                'phone': '+91-9876543214',
                'skills': json.dumps(['Java', 'Spring Boot', 'Hibernate', 'MySQL', 'Docker']),
                'education': json.dumps([
                    {
                        'degree': 'B.Tech Computer Science',
                        'institution': 'DTU Delhi',
                        'year': '2023'
                    }
                ]),
                'experience': json.dumps([
                    {
                        'title': 'Backend Developer',
                        'company': 'Enterprise Solutions',
                        'duration': '2.5 years'
                    }
                ]),
                'projects': json.dumps([
                    {
                        'title': 'REST API Service',
                        'description': 'Microservices-based API',
                        'technologies': ['Spring Boot', 'PostgreSQL', 'Docker'],
                        'duration': '8 months'
                    }
                ]),
                'ats_score': 75,
                'cgpa': '7.5',
                'academic_percentage': '75',
                'graduation_year': '2023',
                'city': 'Delhi',
                'region': 'India'
            }
        ]
        
        for candidate in test_candidates:
            # Check if candidate already exists
            cursor.execute("SELECT id FROM candidate_profiles WHERE email = %s", (candidate['email'],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"ℹ️ Candidate {candidate['name']} already exists, skipping...")
                continue
            
            # Insert new candidate
            cursor.execute("""
                INSERT INTO candidate_profiles 
                (name, email, phone, skills, education, experience, projects, ats_score, 
                 cgpa, academic_percentage, graduation_year, uploaded_at, city, region)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                candidate['name'], candidate['email'], candidate['phone'], candidate['skills'],
                candidate['education'], candidate['experience'], candidate['projects'], candidate['ats_score'],
                candidate['cgpa'], candidate['academic_percentage'], candidate['graduation_year'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), candidate['city'], candidate['region']
            ))
            print(f"✅ Added test candidate: {candidate['name']}")
        
        connection.commit()
        print(f"\n🎉 Successfully added {len(test_candidates)} test candidates with academic data!")
        
    except Exception as e:
        print(f"❌ Error adding test data: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔄 Adding test candidates with academic performance data...")
    add_test_candidates()
    print("✅ Test data addition completed!") 