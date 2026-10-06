"""
Helper script to add candidates to the database
Run this script to add candidates for the election
"""

from app import create_app
from models.voter import db
from models.voting import Candidate

def add_sample_candidates():
    """Add sample candidates for testing"""
    app = create_app()
    
    with app.app_context():
        # Check if candidates already exist
        existing_count = Candidate.query.count()
        if existing_count > 0:
            print(f"⚠ Warning: {existing_count} candidates already exist in database")
            response = input("Do you want to delete existing candidates and add new ones? (y/n): ")
            if response.lower() == 'y':
                Candidate.query.delete()
                db.session.commit()
                print("✓ Existing candidates deleted")
            else:
                print("❌ Operation cancelled")
                return
        
        # Sample candidates data
        candidates_data = [
            {
                'name': 'Rajesh Kumar',
                'party': 'Democratic Party',
                'description': 'Focus on education and healthcare reform',
                'sign_number': 1
            },
            {
                'name': 'Priya Sharma',
                'party': 'People\'s Alliance',
                'description': 'Youth empowerment and technology advancement',
                'sign_number': 2
            },
            {
                'name': 'Arun Singh',
                'party': 'Progressive Front',
                'description': 'Economic development and job creation',
                'sign_number': 3
            },
            {
                'name': 'Meera Patel',
                'party': 'Green Initiative',
                'description': 'Environmental protection and sustainability',
                'sign_number': 4
            },
            {
                'name': 'Vikram Reddy',
                'party': 'Unity Coalition',
                'description': 'Infrastructure development and rural welfare',
                'sign_number': 5
            }
        ]
        
        # Add candidates
        print("\n" + "="*60)
        print("Adding Candidates to Database")
        print("="*60)
        
        for candidate_data in candidates_data:
            candidate = Candidate(**candidate_data)
            db.session.add(candidate)
            print(f"✓ Added: {candidate.name} (Sign: {candidate.sign_number})")
        
        db.session.commit()
        
        print("="*60)
        print(f"✓ Successfully added {len(candidates_data)} candidates")
        print("="*60)
        
        # Display all candidates
        print("\nCurrent Candidates:")
        all_candidates = Candidate.query.order_by(Candidate.sign_number).all()
        for c in all_candidates:
            print(f"  Sign {c.sign_number}: {c.name} ({c.party})")
        print()


def add_custom_candidate():
    """Add a custom candidate interactively"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("Add Custom Candidate")
        print("="*60)
        
        name = input("Candidate Name: ").strip()
        party = input("Party Name: ").strip()
        description = input("Description: ").strip()
        
        # Get next available sign number
        max_sign = db.session.query(db.func.max(Candidate.sign_number)).scalar() or 0
        next_sign = max_sign + 1
        
        if next_sign > 11:
            print("❌ Error: Maximum 11 candidates allowed (signs 1-11)")
            return
        
        print(f"\nAssigned Sign Number: {next_sign}")
        
        confirm = input("\nConfirm adding this candidate? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Cancelled")
            return
        
        candidate = Candidate(
            name=name,
            party=party,
            description=description,
            sign_number=next_sign
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        print(f"\n✓ Successfully added {name} with sign number {next_sign}")


def list_candidates():
    """List all candidates"""
    app = create_app()
    
    with app.app_context():
        candidates = Candidate.query.order_by(Candidate.sign_number).all()
        
        print("\n" + "="*60)
        print("Current Candidates")
        print("="*60)
        
        if not candidates:
            print("No candidates found in database")
        else:
            for c in candidates:
                status = "Active" if c.is_active else "Inactive"
                print(f"\nSign {c.sign_number}: {c.name}")
                print(f"  Party: {c.party}")
                print(f"  Description: {c.description}")
                print(f"  Status: {status}")
                print(f"  Votes: {c.vote_count}")
        
        print("="*60 + "\n")


def delete_all_candidates():
    """Delete all candidates"""
    app = create_app()
    
    with app.app_context():
        count = Candidate.query.count()
        if count == 0:
            print("No candidates to delete")
            return
        
        print(f"\n⚠ Warning: This will delete all {count} candidates")
        confirm = input("Are you sure? Type 'DELETE' to confirm: ")
        
        if confirm == 'DELETE':
            Candidate.query.delete()
            db.session.commit()
            print(f"✓ Deleted all {count} candidates")
        else:
            print("❌ Cancelled")


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║         Candidate Management Utility                 ║
    ╚═══════════════════════════════════════════════════════╝
    
    Options:
    1. Add sample candidates (5 candidates)
    2. Add custom candidate
    3. List all candidates
    4. Delete all candidates
    5. Exit
    """)
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            add_sample_candidates()
        elif choice == '2':
            add_custom_candidate()
        elif choice == '3':
            list_candidates()
        elif choice == '4':
            delete_all_candidates()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")