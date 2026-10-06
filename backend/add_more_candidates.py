"""Add candidates for signs 6-9"""
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

# Additional candidates for signs 6-9
new_candidates = [
    (6, 'Sunita Rao', 'Social Justice Party', 'Equal rights and social welfare programs', True, 0),
    (7, 'Karan Malhotra', 'Innovation Front', 'Digital transformation and startup support', True, 0),
    (8, 'Anjali Verma', 'Education Alliance', 'Quality education and skill development', True, 0),
    (9, 'Arjun Nair', 'Health First Party', 'Universal healthcare and medical infrastructure', True, 0),
]

print("="*60)
print("Adding Candidates for Signs 6-9")
print("="*60)

# Insert new candidates
for sign, name, party, desc, active, votes in new_candidates:
    # Check if candidate with this sign number already exists
    cursor.execute("SELECT name FROM candidate WHERE sign_number = ?", (sign,))
    existing = cursor.fetchone()

    if existing:
        print(f"⚠ Sign {sign} already assigned to {existing[0]} - skipping")
        continue

    cursor.execute("""
        INSERT INTO candidate (sign_number, name, party, description, is_active, vote_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sign, name, party, desc, active, votes))
    print(f"✓ Added: {name} (Sign: {sign})")

conn.commit()

print("="*60)
print("✓ Successfully updated candidates")
print("="*60)

# Display all candidates
print("\nAll Candidates:")
cursor.execute("SELECT sign_number, name, party FROM candidate ORDER BY sign_number")
for row in cursor.fetchall():
    print(f"  Sign {row[0]}: {row[1]} ({row[2]})")

conn.close()
print("\n✓ Done!\n")
