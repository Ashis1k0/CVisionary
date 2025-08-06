import mysql.connector
from sqlalchemy import create_engine, text

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root10',
    'database': 'resume_analysis'
}

def update_database_schema():
    """Add new academic performance columns to the candidate_profiles table"""
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Check if columns already exist
        cursor.execute("DESCRIBE candidate_profiles")
        existing_columns = [column[0] for column in cursor.fetchall()]
        
        # Add new columns if they don't exist
        new_columns = [
            ('cgpa', 'VARCHAR(10)'),
            ('academic_percentage', 'VARCHAR(10)'),
            ('graduation_year', 'VARCHAR(10)')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE candidate_profiles ADD COLUMN {column_name} {column_type}")
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    print(f"❌ Error adding column {column_name}: {e}")
            else:
                print(f"ℹ️ Column {column_name} already exists")
        
        connection.commit()
        print("✅ Database schema updated successfully!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔄 Updating database schema...")
    update_database_schema()
    print("✅ Database update completed!") 