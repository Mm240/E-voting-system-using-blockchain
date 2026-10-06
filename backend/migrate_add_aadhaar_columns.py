"""
Migration script to add aadhaar_image_path and aadhaar_verified columns to biometric_data table
"""
import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'voting.db')

def migrate():
    print(f"Connecting to database: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("Please make sure the backend has been run at least once to create the database.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(biometric_data)")
        columns = [column[1] for column in cursor.fetchall()]

        print(f"\n📋 Current columns in biometric_data table:")
        for col in columns:
            print(f"  - {col}")

        # Add aadhaar_image_path column if it doesn't exist
        if 'aadhaar_image_path' not in columns:
            print("\n➕ Adding aadhaar_image_path column...")
            cursor.execute("""
                ALTER TABLE biometric_data
                ADD COLUMN aadhaar_image_path VARCHAR(255)
            """)
            print("✅ aadhaar_image_path column added successfully")
        else:
            print("\n✓ aadhaar_image_path column already exists")

        # Add aadhaar_verified column if it doesn't exist
        if 'aadhaar_verified' not in columns:
            print("\n➕ Adding aadhaar_verified column...")
            cursor.execute("""
                ALTER TABLE biometric_data
                ADD COLUMN aadhaar_verified BOOLEAN DEFAULT 0
            """)
            print("✅ aadhaar_verified column added successfully")
        else:
            print("\n✓ aadhaar_verified column already exists")

        # Commit changes
        conn.commit()

        # Verify the migration
        cursor.execute("PRAGMA table_info(biometric_data)")
        columns = [column[1] for column in cursor.fetchall()]

        print(f"\n📋 Updated columns in biometric_data table:")
        for col in columns:
            print(f"  - {col}")

        print("\n🎉 Migration completed successfully!")

    except sqlite3.Error as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add Aadhaar Verification Columns")
    print("=" * 60)
    migrate()
