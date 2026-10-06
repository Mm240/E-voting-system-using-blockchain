#!/usr/bin/env python3
"""
Manual Blockchain to Database Sync Script
Use this to sync candidates from blockchain to backend database
"""

import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from web3 import Web3
    import json
except ImportError:
    print("ERROR: web3 library not installed")
    print("Install it with: pip install web3")
    sys.exit(1)

def main():
    print("\n" + "="*70)
    print("Blockchain to Database Sync Utility")
    print("="*70 + "\n")

    # Get configuration
    web3_provider = input("Enter Web3 provider URL [http://127.0.0.1:7545]: ").strip() or "http://127.0.0.1:7545"
    contract_address = input("Enter contract address: ").strip()

    if not contract_address:
        print("ERROR: Contract address is required")
        sys.exit(1)

    # Load contract ABI
    abi_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'frontend',
        'src',
        'abi',
        'Voting.json'
    )

    if not os.path.exists(abi_path):
        print(f"ERROR: Contract ABI not found at {abi_path}")
        sys.exit(1)

    print(f"\nConnecting to blockchain at {web3_provider}...")

    try:
        # Initialize Web3
        web3 = Web3(Web3.HTTPProvider(web3_provider))

        if not web3.is_connected():
            print("ERROR: Cannot connect to blockchain")
            sys.exit(1)

        print("✓ Connected to blockchain")

        # Load contract
        with open(abi_path, 'r') as f:
            contract_json = json.load(f)
            contract_abi = contract_json.get('abi', contract_json)

        contract = web3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=contract_abi
        )

        # Get candidates from blockchain
        candidate_count = contract.functions.candidateCount().call()
        print(f"✓ Found {candidate_count} candidates in blockchain\n")

        if candidate_count == 0:
            print("No candidates to sync")
            sys.exit(0)

        # Display candidates
        print("Blockchain Candidates:")
        print("-" * 70)
        blockchain_candidates = []
        for i in range(1, candidate_count + 1):
            candidate = contract.functions.candidates(i).call()
            candidate_data = {
                'id': int(candidate[0]),
                'name': candidate[1],
                'votes': int(candidate[2])
            }
            blockchain_candidates.append(candidate_data)
            print(f"  {candidate_data['id']}. {candidate_data['name']} (Votes: {candidate_data['votes']})")

        print()

        # Connect to database
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'voting.db')
        print(f"Database: {db_path}")

        if not os.path.exists(db_path):
            print("ERROR: Database not found")
            sys.exit(1)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Show existing database candidates
        cursor.execute("SELECT id, name, sign_number FROM candidates ORDER BY sign_number")
        db_candidates = cursor.fetchall()

        if db_candidates:
            print("\nCurrent Database Candidates:")
            print("-" * 70)
            for row in db_candidates:
                print(f"  ID: {row[0]}, Sign: {row[2]}, Name: {row[1]}")
        else:
            print("\nDatabase has no candidates")

        print("\n" + "="*70)
        action = input("Clear database and sync from blockchain? (yes/no): ").strip().lower()

        if action != 'yes':
            print("Sync cancelled")
            conn.close()
            sys.exit(0)

        # Clear existing candidates
        cursor.execute("DELETE FROM candidates")
        conn.commit()
        print("✓ Cleared existing candidates")

        # Insert blockchain candidates
        print("\nSyncing candidates...")
        for bc_candidate in blockchain_candidates:
            cursor.execute("""
                INSERT INTO candidates (name, party, sign_number, is_active, vote_count)
                VALUES (?, ?, ?, ?, ?)
            """, (
                bc_candidate['name'],
                f"Party {bc_candidate['id']}",  # Default party
                bc_candidate['id'],
                1,  # is_active
                bc_candidate['votes']
            ))
            print(f"  ✓ Added: {bc_candidate['name']} (Sign: {bc_candidate['id']})")

        conn.commit()
        print(f"\n✓ Successfully synced {len(blockchain_candidates)} candidates")

        # Verify
        cursor.execute("SELECT COUNT(*) FROM candidates")
        final_count = cursor.fetchone()[0]
        print(f"✓ Database now has {final_count} candidates")

        conn.close()

        print("\n" + "="*70)
        print("Sync completed successfully!")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
