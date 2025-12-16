"""
Utility script to generate password hashes for use in .env file
Run this to create a secure hash of your admin password
"""
from werkzeug.security import generate_password_hash
import getpass

def generate_hash():
    """Generate a password hash for the admin user"""
    print("=" * 60)
    print("Password Hash Generator for Blog Admin")
    print("=" * 60)
    print()

    # Get password input (hidden for security)
    password = getpass.getpass("Enter admin password: ")
    password_confirm = getpass.getpass("Confirm password: ")

    # Check passwords match
    if password != password_confirm:
        print("\n❌ Error: Passwords do not match!")
        return

    # Check password isn't empty
    if not password:
        print("\n❌ Error: Password cannot be empty!")
        return

    # Generate hash using pbkdf2:sha256 method (Flask default)
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    print("\n✅ Password hash generated successfully!")
    print("\nAdd this line to your .env file:")
    print("-" * 60)
    print(f"ADMIN_PASSWORD_HASH={password_hash}")
    print("-" * 60)
    print("\n⚠️  Security reminder:")
    print("   • Never commit the .env file to git")
    print("   • Keep this hash secret")
    print("   • Delete this terminal output after copying the hash")
    print()

if __name__ == '__main__':
    generate_hash()
