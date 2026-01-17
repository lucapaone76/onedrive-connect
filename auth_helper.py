#!/usr/bin/env python3
"""
OneDrive Authentication Helper

This script helps you authenticate with Microsoft OneDrive and obtain access tokens
for use with the OneDrive Skill.

Requirements:
    pip install msal

Usage:
    python auth_helper.py
"""

import sys
import os
from pathlib import Path

try:
    from msal import PublicClientApplication
except ImportError:
    print("❌ Error: MSAL library not found.")
    print("Please install it with: pip install msal")
    sys.exit(1)


def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("  OneDrive Skill - Authentication Helper")
    print("=" * 70)
    print()
    print("This script will help you authenticate with Microsoft OneDrive")
    print("and obtain access tokens for the OneDrive Skill.")
    print()


def print_instructions():
    """Print setup instructions."""
    print("📋 BEFORE YOU START:")
    print()
    print("1. Go to https://portal.azure.com/")
    print("2. Navigate to: Azure Active Directory > App registrations")
    print("3. Click 'New registration' and create an app with:")
    print("   - Name: OneDrive Skill for Claude")
    print("   - Supported account types: Personal Microsoft accounts")
    print("   - Redirect URI: Public client/native > http://localhost")
    print()
    print("4. In your app, go to 'API permissions' and add:")
    print("   - Microsoft Graph > Delegated permissions:")
    print("     • Files.ReadWrite")
    print("     • User.Read")
    print("     • offline_access (for refresh tokens)")
    print()
    print("5. Copy your 'Application (client) ID' from the Overview page")
    print()
    print("-" * 70)
    print()


def get_client_id():
    """Get client ID from user or environment."""
    # Check if already set in environment
    client_id = os.getenv("AZURE_CLIENT_ID")
    if client_id:
        print(f"ℹ️  Using Client ID from environment: {client_id[:8]}...")
        use_env = input("Use this Client ID? (y/n): ").strip().lower()
        if use_env == 'y':
            return client_id

    # Get from user
    print()
    client_id = input("Enter your Application (client) ID: ").strip()

    if not client_id:
        print("❌ Error: Client ID is required")
        sys.exit(1)

    return client_id


def authenticate(client_id):
    """Perform authentication and get tokens."""
    print()
    print("🔐 Starting authentication...")
    print()

    # Create MSAL application
    app = PublicClientApplication(
        client_id=client_id,
        authority="https://login.microsoftonline.com/common"
    )

    # Required scopes
    scopes = [
        "Files.ReadWrite",
        "User.Read",
        "offline_access"  # Required for refresh tokens
    ]

    print("📱 A browser window will open for you to sign in.")
    print("   Please sign in with your Microsoft account.")
    print()

    # Perform interactive authentication
    result = app.acquire_token_interactive(scopes=scopes)

    return result


def save_tokens(result):
    """Save tokens to .env file."""
    if "access_token" not in result:
        print()
        print("❌ Authentication failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(f"Description: {result.get('error_description', 'No description')}")
        return False

    access_token = result["access_token"]
    refresh_token = result.get("refresh_token")

    print()
    print("=" * 70)
    print("✅ Authentication successful!")
    print("=" * 70)
    print()

    # Display tokens (truncated for security)
    print("📋 Your Tokens:")
    print()
    print("Access Token:")
    print(f"  {access_token[:40]}...{access_token[-20:]}")
    print()

    if refresh_token:
        print("Refresh Token:")
        print(f"  {refresh_token[:40]}...{refresh_token[-20:]}")
        print()

    # Show expiration info
    if "expires_in" in result:
        expires_in = result["expires_in"] // 60  # Convert to minutes
        print(f"⏰ Access token expires in: {expires_in} minutes")
        print()

    # Ask if user wants to save to .env
    print("-" * 70)
    print()
    save_choice = input("Save tokens to .env file? (y/n): ").strip().lower()

    if save_choice == 'y':
        env_path = Path(".env")

        # Read existing .env if it exists
        existing_content = []
        if env_path.exists():
            with open(env_path, 'r') as f:
                existing_content = [
                    line for line in f.readlines()
                    if not line.startswith('ONEDRIVE_ACCESS_TOKEN=')
                    and not line.startswith('ONEDRIVE_REFRESH_TOKEN=')
                ]

        # Write tokens
        with open(env_path, 'w') as f:
            # Write existing content first
            f.writelines(existing_content)

            # Add tokens
            f.write(f"ONEDRIVE_ACCESS_TOKEN={access_token}\n")
            if refresh_token:
                f.write(f"ONEDRIVE_REFRESH_TOKEN={refresh_token}\n")

        print()
        print(f"✅ Tokens saved to {env_path.absolute()}")
        print()
        print("To use with Python:")
        print("  1. pip install python-dotenv")
        print("  2. In your code:")
        print("     from dotenv import load_dotenv")
        print("     load_dotenv()")
        print("     from onedrive_skill import OneDriveSkill")
        print("     skill = OneDriveSkill()")
    else:
        print()
        print("To use these tokens, set them as environment variables:")
        print()
        print("On Linux/Mac:")
        print(f'  export ONEDRIVE_ACCESS_TOKEN="{access_token}"')
        print()
        print("On Windows (PowerShell):")
        print(f'  $env:ONEDRIVE_ACCESS_TOKEN="{access_token}"')

    print()
    print("=" * 70)
    print("🎉 Setup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Install the skill: pip install onedrive-skill")
    print("  2. Test it:")
    print("     python -c \"from onedrive_skill import OneDriveSkill; skill = OneDriveSkill(); print(skill.list_files())\"")
    print()
    print("⚠️  Security reminders:")
    print("  • Access tokens expire after 1 hour")
    print("  • Use refresh tokens to get new access tokens")
    print("  • Never commit .env file to version control")
    print("  • Add .env to your .gitignore file")
    print()

    return True


def main():
    """Main function."""
    print_banner()
    print_instructions()

    # Get client ID
    client_id = get_client_id()

    # Authenticate
    result = authenticate(client_id)

    # Save tokens
    success = save_tokens(result)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("❌ Authentication cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
