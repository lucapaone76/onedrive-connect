"""Example usage of the OneDrive Skill.

This script demonstrates how to use the OneDrive skill to interact with
Microsoft OneDrive. Make sure to set the ONEDRIVE_ACCESS_TOKEN environment
variable before running this script.

To obtain an access token:
1. Register an application in Azure AD
2. Configure API permissions for Microsoft Graph (Files.ReadWrite.All)
3. Generate an access token using OAuth2 flow
4. Set the token in environment: export ONEDRIVE_ACCESS_TOKEN="your_token"
"""

import os
from onedrive_skill import OneDriveSkill, OneDriveClient


def main():
    """Demonstrate basic OneDrive skill operations."""
    
    # Check if access token is set
    if not os.getenv("ONEDRIVE_ACCESS_TOKEN"):
        print("Error: ONEDRIVE_ACCESS_TOKEN environment variable is not set.")
        print("Please set it before running this example.")
        print("\nExample:")
        print('  export ONEDRIVE_ACCESS_TOKEN="your_token_here"')
        return
    
    try:
        # Initialize the skill
        print("Initializing OneDrive skill...")
        skill = OneDriveSkill()
        
        # Get user information
        print("\n1. Getting user information...")
        user_info = skill.client.get_user_info()
        print(f"   Logged in as: {user_info.get('displayName')} ({user_info.get('userPrincipalName')})")
        
        # List files in root
        print("\n2. Listing files in root directory...")
        files = skill.list_files()
        print(files)
        
        # Search for files
        print("\n3. Searching for documents...")
        search_results = skill.search("document")
        print(search_results)
        
        # Example: Upload a text file
        print("\n4. Uploading a test file...")
        test_content = b"Hello from OneDrive Skill!"
        upload_result = skill.upload_content("test_file.txt", test_content)
        print(f"   {upload_result}")
        
        # Example: Create a folder
        print("\n5. Creating a test folder...")
        folder = skill.client.create_folder("TestFolder")
        print(f"   Created folder: {folder.get('name')} (ID: {folder.get('id')})")
        
        print("\n✓ All operations completed successfully!")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your access token is valid and has the necessary permissions.")


if __name__ == "__main__":
    main()
