"""
Script to delete a voter registration by wallet address
Useful for testing or if you need to re-register
"""
import sys
from app import app
from models.voter import db, Voter, BiometricData, OTP, AuditLog

def delete_voter(wallet_address):
    """Delete a voter and all related data"""
    with app.app_context():
        wallet_address = wallet_address.lower()

        voter = Voter.query.filter_by(wallet_address=wallet_address).first()

        if not voter:
            print(f"❌ No voter found with wallet address: {wallet_address}")
            return False

        print(f"\n📋 Found voter:")
        print(f"   ID: {voter.id}")
        print(f"   Name: {voter.name}")
        print(f"   Aadhaar: {voter.mask_aadhaar()}")
        print(f"   Wallet: {voter.wallet_address}")

        # Confirm deletion
        confirm = input(f"\n⚠️  Are you sure you want to delete this voter? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Deletion cancelled")
            return False

        try:
            # Delete related biometric data
            biometric_count = BiometricData.query.filter_by(voter_id=voter.id).delete()
            print(f"✅ Deleted {biometric_count} biometric record(s)")

            # Delete related OTPs
            otp_count = OTP.query.filter_by(voter_id=voter.id).delete()
            print(f"✅ Deleted {otp_count} OTP record(s)")

            # Note: AuditLog entries are kept for security/compliance

            # Delete voter
            db.session.delete(voter)
            db.session.commit()

            print(f"\n✅ Voter {wallet_address} deleted successfully!")
            print(f"✅ You can now re-register this wallet address")
            return True

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error deleting voter: {str(e)}")
            return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python delete_voter.py <wallet_address>")
        print("Example: python delete_voter.py 0x1234567890abcdef...")
        sys.exit(1)

    wallet_address = sys.argv[1]
    delete_voter(wallet_address)
