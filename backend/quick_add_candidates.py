"""Quick script to add sample candidates"""
import os
import sys

# Set the database path
db_path = 'voting.db'

# Check if database exists
if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    sys.exit(1)

import sqlite3

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample candidates
candidates = [
    (1, 'Rajesh Kumar', 'Democratic Party', 'Focus on education and healthcare reform', True, 0),
    (2, 'Priya Sharma', 'People\'s Alliance', 'Youth empowerment and technology advancement', True, 0),
    (3, 'Arun Singh', 'Progressive Front', 'Economic development and job creation', True, 0),
    (4, 'Meera Patel', 'Green Initiative', 'Environmental protection and sustainability', True, 0),
    (5, 'Vikram Reddy', 'Unity Coalition', 'Infrastructure development and rural welfare', True, 0),
]

print("="*60)
print("Adding Sample Candidates")
print("="*60)

# Check if candidates already exist
cursor.execute("SELECT COUNT(*) FROM candidate")
count = cursor.fetchone()[0]

if count > 0:
    print(f"\nWarning: {count} candidates already exist")
    response = input("Delete existing and add new? (y/n): ")
    if response.lower() == 'y':
        cursor.execute("DELETE FROM candidate")
        conn.commit()
        print("✓ Existing candidates deleted")
    else:
        print("❌ Cancelled")
        conn.close()
        sys.exit(0)

# Insert candidates
for sign, name, party, desc, active, votes in candidates:
    cursor.execute("""
        INSERT INTO candidate (sign_number, name, party, description, is_active, vote_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sign, name, party, desc, active, votes))
    print(f"✓ Added: {name} (Sign: {sign})")

conn.commit()

print("="*60)
print(f"✓ Successfully added {len(candidates)} candidates")
print("="*60)

# Display all candidates
print("\nCurrent Candidates:")
cursor.execute("SELECT sign_number, name, party FROM candidate ORDER BY sign_number")
for row in cursor.fetchall():
    print(f"  Sign {row[0]}: {row[1]} ({row[2]})")

conn.close()
print("\n✓ Done!\n")
