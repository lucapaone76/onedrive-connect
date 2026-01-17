"""Example usage of the OneDrive Skill.

This script demonstrates how to use the OneDrive skill to interact with
Microsoft OneDrive. Make sure to set the ONEDRIVE_ACCESS_TOKEN environment
variable before running this script.

To obtain an access token:
1. Register an application in Azure AD
2. Configure API permissions for Microsoft Graph (Files.ReadWrite.All)
3. Generate an access token using OAuth2 flow
4. Set the token in environment: export ONEDRIVE_ACCESS_TOKEN="your_token"

This example demonstrates the safety features including user confirmation
for destructive operations.
"""

import os
from onedrive_skill import OneDriveSkill, OneDriveClient


def custom_confirmation(message: str) -> bool:
    """Custom confirmation handler for automated testing.
    
    In production, this would prompt the user for confirmation.
    For this example, we'll auto-approve read operations and
    require explicit approval for destructive operations.
    """
    print(f"\n{message}")
    # For demo purposes, automatically decline destructive operations
    if "DELETE" in message or "OVERWRITE" in message:
        print("(Auto-declining destructive operation for safety)")
        return False
    return True


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
        # Initialize the skill with custom confirmation handler
        print("Initializing OneDrive skill...")
        print("(Using custom confirmation handler for safety demonstration)")
        skill = OneDriveSkill(confirmation_callback=custom_confirmation)
        
        # Display skill metadata
        print("\n📋 Skill Metadata:")
        metadata = skill.get_skill_metadata()
        print(f"   Name: {metadata.get('name')}")
        print(f"   Version: {metadata.get('version')}")
        print(f"   Description: {metadata.get('description')}")
        
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
        
        # Example: Upload a text file (with confirmation)
        print("\n4. Uploading a test file (requires confirmation)...")
        test_content = b"Hello from OneDrive Skill!"
        upload_result = skill.upload_content("test_file.txt", test_content)
        print(f"   {upload_result}")
        
        # Example: Create a folder
        print("\n5. Creating a test folder...")
        folder_result = skill.create_folder("TestFolder")
        print(f"   {folder_result}")
        
        # Example: Demonstrate delete with confirmation (will be declined)
        print("\n6. Attempting to delete a file (requires confirmation)...")
        print("   (This will be automatically declined for safety in this demo)")
        # Uncomment the following line to actually test deletion:
        # delete_result = skill.delete_item("file_id_here", "test_file.txt")
        # print(f"   {delete_result}")
        
        print("\n✓ All operations completed successfully!")
        print("\n📌 Safety Features Demonstrated:")
        print("   ✓ User confirmation required for file uploads")
        print("   ✓ User confirmation required for deletions")
        print("   ✓ Clear warnings for destructive operations")
        print("   ✓ Ability to cancel operations before execution")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your access token is valid and has the necessary permissions.")


if __name__ == "__main__":
    main()
