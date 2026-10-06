"""Initialize database and add candidates without running full app"""
import sqlite3
import os

db_path = 'instance/voting.db'

print("="*60)
print("Initializing Database")
print("="*60)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create candidates table
print("Creating candidates table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    symbol VARCHAR(255),
    description TEXT,
    sign_number INTEGER UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    vote_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create votes table
print("Creating votes table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    vote_method VARCHAR(20) NOT NULL,
    detected_sign INTEGER,
    confidence_score REAL,
    sign_image_path VARCHAR(255),
    transaction_hash VARCHAR(66) UNIQUE,
    block_number INTEGER,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
)
""")

conn.commit()
print("✓ Tables created")

# Sample candidates
candidates = [
    (1, 'Rajesh Kumar', 'Democratic Party', 'Focus on education and healthcare reform', 1, 0),
    (2, 'Priya Sharma', "People's Alliance", 'Youth empowerment and technology advancement', 1, 0),
    (3, 'Arun Singh', 'Progressive Front', 'Economic development and job creation', 1, 0),
    (4, 'Meera Patel', 'Green Initiative', 'Environmental protection and sustainability', 1, 0),
    (5, 'Vikram Reddy', 'Unity Coalition', 'Infrastructure development and rural welfare', 1, 0),
]

print("\n" + "="*60)
print("Adding Sample Candidates")
print("="*60)

# Check if candidates already exist
cursor.execute("SELECT COUNT(*) FROM candidates")
count = cursor.fetchone()[0]

if count > 0:
    print(f"\nWarning: {count} candidates already exist")
    print("Deleting existing candidates...")
    cursor.execute("DELETE FROM candidates")
    conn.commit()
    print("✓ Existing candidates deleted")

# Insert candidates
for sign, name, party, desc, active, votes in candidates:
    cursor.execute("""
        INSERT INTO candidates (sign_number, name, party, description, is_active, vote_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sign, name, party, desc, active, votes))
    print(f"✓ Added: {name} (Sign: {sign})")

conn.commit()

print("="*60)
print(f"✓ Successfully added {len(candidates)} candidates")
print("="*60)

# Display all candidates
print("\nCurrent Candidates:")
cursor.execute("SELECT sign_number, name, party, is_active FROM candidates ORDER BY sign_number")
for row in cursor.fetchall():
    status = "Active" if row[3] else "Inactive"
    print(f"  Sign {row[0]}: {row[1]} ({row[2]}) - {status}")

conn.close()
print("\n✓ Database initialized successfully!\n")
