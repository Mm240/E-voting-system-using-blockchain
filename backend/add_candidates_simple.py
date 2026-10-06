"""Simple script to add candidates directly to the database"""
import sqlite3
import os

# Path to the database file
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'voting.db')

print(f"Using database: {db_path}")
print("\n" + "="*60)
print("Candidate Management - Simple")
print("="*60 + "\n")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Show current candidates
print("Current Candidates:")
cursor.execute("SELECT id, name, party, sign_number, is_active FROM candidates ORDER BY sign_number")
current = cursor.fetchall()
if current:
    for row in current:
        print(f"  ID: {row[0]}, Sign: {row[3]}, Name: {row[1]}, Party: {row[2]}, Active: {row[4]}")
else:
    print("  No candidates found")

print("\n" + "="*60)
print("Options:")
print("1. Clear all candidates and add new ones")
print("2. Add a single candidate")
print("3. Delete all candidates")
print("4. Exit")
print("="*60 + "\n")

choice = input("Enter your choice (1-4): ").strip()

if choice == '1':
    # Clear existing
    cursor.execute("DELETE FROM candidates")
    conn.commit()
    print("\n✓ Cleared all existing candidates\n")

    # Get number of candidates to add
    num = int(input("How many candidates do you want to add? "))

    for i in range(1, num + 1):
        print(f"\nCandidate {i}:")
        name = input("  Name: ").strip()
        party = input("  Party: ").strip()
        description = input("  Description (optional): ").strip() or None

        cursor.execute("""
            INSERT INTO candidates (name, party, description, sign_number, is_active, vote_count)
            VALUES (?, ?, ?, ?, 1, 0)
        """, (name, party, description, i))
        print(f"  ✓ Added: {name} (Sign: {i})")

    conn.commit()
    print(f"\n✓ Successfully added {num} candidates")

elif choice == '2':
    # Get next available sign number
    cursor.execute("SELECT MAX(sign_number) FROM candidates")
    max_sign = cursor.fetchone()[0]
    next_sign = (max_sign or 0) + 1

    if next_sign > 11:
        print("❌ Error: Maximum 11 candidates allowed")
    else:
        print(f"\nNew Candidate (Sign: {next_sign}):")
        name = input("  Name: ").strip()
        party = input("  Party: ").strip()
        description = input("  Description (optional): ").strip() or None

        cursor.execute("""
            INSERT INTO candidates (name, party, description, sign_number, is_active, vote_count)
            VALUES (?, ?, ?, ?, 1, 0)
        """, (name, party, description, next_sign))
        conn.commit()
        print(f"\n✓ Added: {name} (Sign: {next_sign})")

elif choice == '3':
    confirm = input("Are you sure you want to delete ALL candidates? Type 'YES' to confirm: ")
    if confirm == 'YES':
        cursor.execute("DELETE FROM candidates")
        conn.commit()
        print("\n✓ Deleted all candidates")
    else:
        print("\n❌ Cancelled")

elif choice == '4':
    print("\nGoodbye!")
else:
    print("\n❌ Invalid choice")

# Show final state
print("\n" + "="*60)
print("Final Candidate List:")
cursor.execute("SELECT id, name, party, sign_number FROM candidates ORDER BY sign_number")
for row in cursor.fetchall():
    print(f"  Sign {row[3]}: {row[1]} ({row[2]})")
print("="*60 + "\n")

conn.close()
