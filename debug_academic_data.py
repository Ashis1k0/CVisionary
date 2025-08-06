import mysql.connector
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root10',
    'database': 'resume_analysis'
}

def check_academic_data():
    """Check what academic data is stored in the database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Get all candidates with their academic data
        cursor.execute("""
            SELECT id, name, email, ats_score, cgpa, academic_percentage, graduation_year, education
            FROM candidate_profiles
            ORDER BY id DESC
            LIMIT 10
        """)
        
        candidates = cursor.fetchall()
        
        print("📊 Academic Data Analysis:")
        print("=" * 80)
        
        for candidate in candidates:
            print(f"\n👤 Candidate: {candidate[1]} ({candidate[2]})")
            print(f"   ATS Score: {candidate[3]}%")
            print(f"   CGPA: {candidate[4] if candidate[4] else 'Not available'}")
            print(f"   Academic %: {candidate[5] if candidate[5] else 'Not available'}")
            print(f"   Graduation Year: {candidate[6] if candidate[6] else 'Not available'}")
            
            # Parse education data to see what's available
            if candidate[7]:
                try:
                    education_data = json.loads(candidate[7])
                    print(f"   Education Data: {json.dumps(education_data, indent=2)}")
                except:
                    print(f"   Education Data: {candidate[7]}")
        
        # Count candidates with academic data
        cursor.execute("""
            SELECT 
                COUNT(*) as total_candidates,
                COUNT(CASE WHEN cgpa IS NOT NULL AND cgpa != '' THEN 1 END) as with_cgpa,
                COUNT(CASE WHEN academic_percentage IS NOT NULL AND academic_percentage != '' THEN 1 END) as with_percentage,
                COUNT(CASE WHEN graduation_year IS NOT NULL AND graduation_year != '' THEN 1 END) as with_year
            FROM candidate_profiles
        """)
        
        stats = cursor.fetchone()
        print(f"\n📈 Statistics:")
        print(f"   Total Candidates: {stats[0]}")
        print(f"   With CGPA: {stats[1]}")
        print(f"   With Academic %: {stats[2]}")
        print(f"   With Graduation Year: {stats[3]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    check_academic_data() 