# OneDrive Connect - LLM Skill

A Python project to provide a skill (in the sense of the standard skills now available for LLMs) to connect to personal Microsoft OneDrive. Authentication tokens are injected via environment variables or secrets for security.

## Features

- 🔐 Secure authentication via environment variables
- 📁 List files and folders in OneDrive
- ⬆️ Upload files to OneDrive
- ⬇️ Download files from OneDrive
- 🔍 Search for files across OneDrive
- 📂 Create and manage folders
- 🗑️ Delete items
- 🤖 LLM-friendly skill interface

## Installation

### From source

```bash
git clone https://github.com/lucapaone76/onedrive-connect.git
cd onedrive-connect
pip install -r requirements.txt
```

### Using pip (after publishing)

```bash
pip install onedrive-skill
```

## Authentication Setup

This skill uses the Microsoft Graph API to connect to OneDrive. You need to obtain an access token:

### Step 1: Register an Application in Azure AD

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Name your application (e.g., "OneDrive Skill")
5. Select appropriate account type (Personal Microsoft accounts for personal OneDrive)
6. Click **Register**

### Step 2: Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission** > **Microsoft Graph** > **Delegated permissions**
3. Add the following permissions:
   - `Files.ReadWrite` (or `Files.ReadWrite.All` for broader access)
   - `User.Read`
4. Click **Add permissions**
5. Click **Grant admin consent** if applicable

### Step 3: Generate Access Token

You can generate an access token using various OAuth2 flows. For testing purposes, you can use:

- **Azure AD OAuth2 authorization code flow**
- **Device code flow**
- **MSAL (Microsoft Authentication Library)**

Example using MSAL (Python):

```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="YOUR_CLIENT_ID",
    authority="https://login.microsoftonline.com/common"
)

# Interactive authentication
result = app.acquire_token_interactive(
    scopes=["Files.ReadWrite", "User.Read"]
)

if "access_token" in result:
    access_token = result["access_token"]
    print(f"Access token: {access_token}")
```

### Step 4: Set Environment Variable

```bash
export ONEDRIVE_ACCESS_TOKEN="your_access_token_here"
```

Or create a `.env` file (see `.env.example`):

```bash
cp .env.example .env
# Edit .env and add your access token
```

**⚠️ Security Note:** Never commit your `.env` file or access tokens to version control!

## Usage

### Basic Usage with OneDriveClient

```python
from onedrive_skill import OneDriveClient

# Initialize client (uses ONEDRIVE_ACCESS_TOKEN from environment)
client = OneDriveClient()

# Or provide token explicitly
client = OneDriveClient(access_token="your_token")

# Get user information
user = client.get_user_info()
print(f"Logged in as: {user['displayName']}")

# List files in root
items = client.list_root_items()
for item in items:
    print(f"- {item['name']}")

# Upload a file
with open("example.txt", "rb") as f:
    result = client.upload_file("Documents/example.txt", f.read())
    print(f"Uploaded: {result['name']}")

# Download a file
content = client.download_file(item_id="FILE_ID")
with open("downloaded.txt", "wb") as f:
    f.write(content)

# Search for files
results = client.search_items("quarterly report")
for item in results:
    print(f"Found: {item['name']}")
```

### Using the OneDriveSkill (LLM-Friendly Interface)

```python
from onedrive_skill import OneDriveSkill

# Initialize skill
skill = OneDriveSkill()

# List files (returns formatted string)
print(skill.list_files())
# Output:
# - [File] document.docx (12345 bytes)
# - [Folder] Photos (0 bytes)
# - [File] report.pdf (98765 bytes)

# Search for items
print(skill.search("budget"))
# Output:
# Found 3 item(s):
# - [File] budget_2024.xlsx (ID: ABC123)
# - [File] budget_proposal.docx (ID: DEF456)
# - [Folder] Budget Archive (ID: GHI789)

# Upload content
content = b"Hello, OneDrive!"
result = skill.upload_content("test.txt", content)
print(result)
# Output: File uploaded successfully: test.txt (ID: XYZ999)
```

### Running the Example

```bash
# Set your access token
export ONEDRIVE_ACCESS_TOKEN="your_token"

# Run the example
python example_usage.py
```

## API Reference

### OneDriveClient

Main client for interacting with OneDrive via Microsoft Graph API.

**Methods:**
- `get_user_info()` - Get authenticated user information
- `list_root_items()` - List items in root directory
- `list_items(folder_path)` - List items in a specific folder
- `get_item_info(item_id)` - Get information about an item
- `download_file(item_id)` - Download a file
- `upload_file(file_path, content, overwrite)` - Upload a file
- `create_folder(folder_name, parent_path)` - Create a new folder
- `delete_item(item_id)` - Delete an item
- `search_items(query)` - Search for items

### OneDriveSkill

Simplified skill interface for LLM integration.

**Methods:**
- `list_files(folder_path)` - List files with formatted output
- `get_file_content(item_id)` - Download file content
- `upload_content(file_path, content)` - Upload file with status message
- `search(query)` - Search with formatted results

## Security Considerations

1. **Never hardcode access tokens** in your code
2. **Use environment variables** or secure secret management systems
3. **Rotate tokens regularly** - access tokens expire and should be refreshed
4. **Limit API permissions** to only what's necessary
5. **Use `.gitignore`** to prevent committing sensitive files
6. **Consider using refresh tokens** for long-lived applications

## Development

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black onedrive_skill/
ruff check onedrive_skill/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

### "No access token provided" Error

Make sure you've set the `ONEDRIVE_ACCESS_TOKEN` environment variable:

```bash
export ONEDRIVE_ACCESS_TOKEN="your_token"
```

### "401 Unauthorized" Error

Your access token may have expired. Generate a new token and update the environment variable.

### "403 Forbidden" Error

Check that your application has the necessary API permissions in Azure AD and that admin consent has been granted if required.

## Related Links

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [OneDrive API Reference](https://docs.microsoft.com/en-us/graph/api/resources/onedrive)
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
