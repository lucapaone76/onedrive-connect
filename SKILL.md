# OneDrive Connect Skill

## Skill Information

**Name**: onedrive-connect
**Version**: 0.1.1
**Author**: lucapaone76
**License**: MIT
**Category**: File Management, Cloud Storage
**Tags**: onedrive, microsoft, graph-api, cloud, storage, files

## Quick Reference

📦 **PyPI Package**: https://pypi.org/project/onedrive-skill/

**Installation**:
```bash
pip install onedrive-skill[auth]  # Includes authentication tools
```

**Quick Setup**:
```bash
python auth_helper.py  # Get your access token
export ONEDRIVE_ACCESS_TOKEN="your_token"
```

**Usage**:
```python
from onedrive_skill import OneDriveSkill
skill = OneDriveSkill()
print(skill.list_files())
```

## Description

A Python skill for LLM systems to interact with personal Microsoft OneDrive accounts via the Microsoft Graph API. This skill provides secure, type-safe operations for file and folder management with built-in safety features and user confirmation for destructive operations.

## Capabilities

This skill provides the following capabilities:

### Read Operations (Safe)
- **list_files**: List files and folders in a OneDrive directory
- **search**: Search for files across OneDrive
- **get_file_content**: Download and retrieve file content

### Write Operations (Requires Confirmation)
- **upload_content**: Upload files to OneDrive (overwrites existing files)
- **create_folder**: Create new folders with configurable conflict resolution

### Destructive Operations (Mandatory Confirmation)
- **delete_item**: Permanently delete files or folders from OneDrive

## Authentication

This skill uses OAuth2 authentication via Microsoft Graph API to access personal OneDrive accounts.

### Authentication Overview

**Type**: OAuth2 Bearer Token
**Provider**: Microsoft Graph API
**Required Scopes**:
- `Files.ReadWrite` or `Files.ReadWrite.All` - Read and write access to files
- `User.Read` - Access to user profile information
- `offline_access` - (Recommended) For refresh token support

**Environment Variable**: `ONEDRIVE_ACCESS_TOKEN`

### Quick Start Authentication

**For Personal Microsoft/OneDrive Accounts:**

1. **Install authentication dependencies**:
   ```bash
   pip install onedrive-skill[auth]
   ```

2. **Run the authentication helper**:
   ```bash
   python auth_helper.py
   ```

   This interactive script will:
   - Guide you through Azure AD app registration
   - Open a browser for Microsoft sign-in
   - Generate access and refresh tokens
   - Save tokens to `.env` file

3. **Set the environment variable**:
   ```bash
   export ONEDRIVE_ACCESS_TOKEN="your_token_here"
   ```

### Detailed Authentication Setup

#### Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: `OneDrive Skill for Claude` (or your preferred name)
   - **Supported account types**: Personal Microsoft accounts
   - **Redirect URI**: `Public client/native (mobile & desktop)` → `http://localhost`
5. Save the **Application (client) ID**

#### Step 2: Configure Permissions

1. In your app, go to **API permissions**
2. Add **Microsoft Graph** → **Delegated permissions**:
   - `Files.ReadWrite`
   - `User.Read`
   - `offline_access`
3. Grant admin consent if prompted

#### Step 3: Generate Tokens

**Option A: Use the Auth Helper Script** (Recommended)

The repository includes `auth_helper.py` for easy token generation:

```bash
python auth_helper.py
```

**Option B: Manual Token Generation**

Use MSAL (Microsoft Authentication Library):

```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="YOUR_CLIENT_ID",
    authority="https://login.microsoftonline.com/common"
)

result = app.acquire_token_interactive(
    scopes=["Files.ReadWrite", "User.Read", "offline_access"]
)

if "access_token" in result:
    access_token = result["access_token"]
    refresh_token = result.get("refresh_token")
```

### Token Management

**Access Token Expiration**: Access tokens expire after **1 hour**.

**Using Refresh Tokens**: To avoid re-authenticating every hour, save and use refresh tokens:

```python
from msal import PublicClientApplication

app = PublicClientApplication(client_id="YOUR_CLIENT_ID", authority="https://login.microsoftonline.com/common")

result = app.acquire_token_by_refresh_token(
    refresh_token="your_refresh_token",
    scopes=["Files.ReadWrite", "User.Read"]
)

new_access_token = result["access_token"]
```

### Security Best Practices

- ✅ Never hardcode tokens in source code
- ✅ Use environment variables or `.env` files
- ✅ Add `.env` to `.gitignore`
- ✅ Rotate tokens regularly
- ✅ Store refresh tokens securely
- ✅ Use dedicated Azure AD app for production
- ⚠️ Access tokens expire after 1 hour
- ⚠️ Refresh tokens have longer lifespan but can be revoked

## Installation

### From PyPI (Recommended)

```bash
# Basic installation
pip install onedrive-skill

# With authentication helper dependencies
pip install onedrive-skill[auth]

# With development dependencies
pip install onedrive-skill[dev]
```

### From Source

```bash
# Clone the repository
git clone https://github.com/lucapaone76/onedrive-connect.git
cd onedrive-connect

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### PyPI Package

**Package Name**: `onedrive-skill`
**PyPI URL**: https://pypi.org/project/onedrive-skill/

## Using with Claude and LLM Systems

This skill is designed to work seamlessly with Claude (Claude.ai, Claude Code CLI) and other LLM systems.

### Setup for Claude

1. **Install the skill**:
   ```bash
   pip install onedrive-skill[auth]
   ```

2. **Authenticate and get token**:
   ```bash
   python auth_helper.py
   ```

3. **Set environment variable** before running Claude:
   ```bash
   export ONEDRIVE_ACCESS_TOKEN="your_token_here"
   ```

4. **Use with Claude**: The skill is now available for Claude to use!

### Example Claude Prompts

Once configured, you can use natural language prompts with Claude:

- "List all files in my OneDrive root folder"
- "Search for PDF files containing 'invoice' in my OneDrive"
- "Upload this document to my OneDrive Documents folder"
- "Create a new folder called 'Project Reports' in OneDrive"
- "Show me all Excel files in my OneDrive"
- "Find all files modified in the last week"

### LLM Integration

The skill provides metadata for LLM discovery and understanding:

```python
from onedrive_skill import OneDriveSkill

skill = OneDriveSkill()

# Get skill metadata for LLM
metadata = skill.get_skill_metadata()
# Returns: capabilities, safety levels, parameters, descriptions
```

This metadata helps LLMs understand:
- What operations are available
- Which operations require user confirmation
- Safety levels of each operation
- Expected parameters and return values

## Usage

### Basic Usage

```python
from onedrive_skill import OneDriveSkill

# Initialize the skill
skill = OneDriveSkill()

# List files in root directory
print(skill.list_files())

# Search for files
print(skill.search("quarterly report"))

# Upload a file (requires confirmation)
content = b"Hello, OneDrive!"
result = skill.upload_content("test.txt", content)
```

### With Custom Confirmation Handler

```python
def custom_confirmation(message: str) -> bool:
    # Integrate with your UI/LLM system
    return get_user_response(message)

skill = OneDriveSkill(confirmation_callback=custom_confirmation)
```

## Safety Features

### User Confirmation Required

This skill implements safety measures for destructive operations:

- **Upload Operations**: Warns users before overwriting existing files
- **Delete Operations**: Requires explicit confirmation before permanent deletion
- **Cancellation Support**: All confirmations can be declined to abort operations

### Safety Levels

- 🟢 **Read-Only**: `list_files`, `search`, `get_file_content`
- 🟡 **Write**: `create_folder`
- 🔴 **Destructive**: `upload_content`, `delete_item`

## API Reference

### list_files(folder_path: str = "") -> str

List files and folders in a OneDrive directory.

**Parameters**:
- `folder_path` (string, optional): Path to the folder to list. Empty string for root.

**Returns**: Formatted string with file listing

**Safety Level**: Read-only

**Example**:
```python
files = skill.list_files("Documents/Projects")
```

### search(query: str) -> str

Search for files in OneDrive.

**Parameters**:
- `query` (string, required): Search query string

**Returns**: Formatted string with search results

**Safety Level**: Read-only

**Example**:
```python
results = skill.search("budget 2024")
```

### get_file_content(item_id: str) -> bytes

Download and retrieve file content from OneDrive.

**Parameters**:
- `item_id` (string, required): The ID of the file to download

**Returns**: File content as bytes

**Safety Level**: Read-only

**Example**:
```python
content = skill.get_file_content("ABC123XYZ")
```

### upload_content(file_path: str, content: bytes, require_confirmation: bool = True) -> str

Upload content to OneDrive.

**WARNING**: This operation will overwrite any existing file at the specified path.

**Parameters**:
- `file_path` (string, required): Path where to upload the file
- `content` (bytes, required): File content as bytes
- `require_confirmation` (boolean, optional): Whether to require user confirmation (default: True)

**Returns**: Success message with file information or cancellation message

**Safety Level**: Destructive (overwrites)

**Example**:
```python
content = b"Hello, World!"
result = skill.upload_content("Documents/hello.txt", content)
```

### create_folder(folder_name: str, parent_path: str = "", conflict_behavior: str = "rename") -> str

Create a new folder in OneDrive.

**Parameters**:
- `folder_name` (string, required): Name of the folder to create
- `parent_path` (string, optional): Path to parent folder (empty for root)
- `conflict_behavior` (string, optional): How to handle naming conflicts - "rename" (default), "replace", or "fail"

**Returns**: Success message with folder information

**Safety Level**: Write

**Example**:
```python
result = skill.create_folder("ProjectFiles", "Documents")
```

### delete_item(item_id: str, item_name: str = None, require_confirmation: bool = True) -> str

Delete a file or folder from OneDrive.

**⚠️ WARNING**: This is a DESTRUCTIVE operation that permanently deletes the item and cannot be undone.

**Parameters**:
- `item_id` (string, required): The ID of the item to delete
- `item_name` (string, optional): Name of the item for better confirmation message
- `require_confirmation` (boolean, optional): Whether to require user confirmation (default: True)

**Returns**: Success message or cancellation message

**Safety Level**: Destructive

**Example**:
```python
result = skill.delete_item("ABC123", "old_file.txt")
```

### get_skill_metadata() -> dict

Get skill metadata for LLM discovery.

**Returns**: Dictionary containing skill metadata including available operations, parameters, safety levels, and descriptions.

**Example**:
```python
metadata = skill.get_skill_metadata()
print(f"Skill: {metadata['name']} v{metadata['version']}")
```

## Error Handling

The skill raises exceptions for common error scenarios:

- `ValueError`: Missing or invalid access token
- `requests.exceptions.HTTPError`: API request failures (401, 403, 404, etc.)
- `OSError`: File system errors when loading manifest

## Configuration

### Environment Variables

#### Required

- `ONEDRIVE_ACCESS_TOKEN`: OAuth2 access token for Microsoft Graph API
  - Obtain using `python auth_helper.py`
  - Expires after 1 hour
  - Must be refreshed periodically

#### Optional

- `ONEDRIVE_REFRESH_TOKEN`: Refresh token for automatic access token renewal
  - Obtained from `auth_helper.py` along with access token
  - Lasts longer than access tokens
  - Used to get new access tokens without re-authenticating

- `AZURE_CLIENT_ID`: Your Azure AD Application (client) ID
  - Useful for automated token refresh
  - From Azure Portal → App registrations → Your app → Overview

- `ONEDRIVE_API_BASE_URL`: Custom API endpoint
  - Default: `https://graph.microsoft.com/v1.0`
  - Only change for special requirements

### Configuration Methods

#### Method 1: Environment Variables

**Linux/Mac:**
```bash
export ONEDRIVE_ACCESS_TOKEN="your_access_token_here"
export ONEDRIVE_REFRESH_TOKEN="your_refresh_token_here"
```

**Windows (PowerShell):**
```powershell
$env:ONEDRIVE_ACCESS_TOKEN="your_access_token_here"
$env:ONEDRIVE_REFRESH_TOKEN="your_refresh_token_here"
```

#### Method 2: .env File (Recommended)

1. Copy the template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your tokens:
   ```bash
   ONEDRIVE_ACCESS_TOKEN=your_access_token_here
   ONEDRIVE_REFRESH_TOKEN=your_refresh_token_here
   AZURE_CLIENT_ID=your_client_id_here
   ```

3. Load in Python:
   ```python
   from dotenv import load_dotenv
   load_dotenv()

   from onedrive_skill import OneDriveSkill
   skill = OneDriveSkill()  # Automatically uses environment variables
   ```

4. **Important**: Add `.env` to `.gitignore`!

#### Method 3: Direct Token Passing

```python
from onedrive_skill import OneDriveSkill

# Pass token directly (not recommended for production)
skill = OneDriveSkill(access_token="your_access_token_here")
```

## Dependencies

### Core Dependencies

- `requests>=2.31.0`: HTTP library for Microsoft Graph API calls

### Optional Dependencies

#### Authentication Helpers (`pip install onedrive-skill[auth]`)

- `msal>=1.20.0`: Microsoft Authentication Library for token generation
  - Required for `auth_helper.py` script
  - Used for OAuth2 authentication flow
  - Handles token acquisition and refresh
- `python-dotenv>=1.0.0`: Load environment variables from .env file
  - Convenient for managing tokens
  - Keeps secrets out of source code

#### Development Tools (`pip install onedrive-skill[dev]`)

- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Code coverage reporting
- `black>=23.0.0`: Code formatter
- `ruff>=0.1.0`: Fast Python linter

### Installing Dependencies

```bash
# Core only
pip install onedrive-skill

# With authentication tools
pip install onedrive-skill[auth]

# With development tools
pip install onedrive-skill[dev]

# All extras
pip install onedrive-skill[auth,dev]
```

## Platform Support

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Linux, macOS, Windows
- **Architecture**: x86_64, ARM64

## Security Considerations

1. **Never hardcode access tokens** in your code
2. **Use environment variables** or secure secret management systems
3. **Rotate tokens regularly** - access tokens expire and should be refreshed
4. **Limit API permissions** to only what's necessary
5. **Use `.gitignore`** to prevent committing sensitive files
6. **User confirmation** is enabled by default for destructive operations

## Limitations

- Requires active internet connection
- Depends on Microsoft Graph API availability
- Access tokens have expiration times
- Rate limits apply based on Microsoft Graph API quotas
- Large file uploads may require resumable upload sessions (not yet implemented)

## Troubleshooting

### "No access token provided" Error

Set the environment variable:
```bash
export ONEDRIVE_ACCESS_TOKEN="your_token"
```

### "401 Unauthorized" Error

Your access token may have expired. Generate a new token and update the environment variable.

### "403 Forbidden" Error

Check that your application has the necessary API permissions in Azure AD and that admin consent has been granted if required.

## Support

- **Documentation**: [README.md](README.md)
- **Requirements**: [REQUIREMENTS.md](REQUIREMENTS.md)
- **Issues**: [GitHub Issues](https://github.com/lucapaone76/onedrive-connect/issues)
- **Repository**: [GitHub](https://github.com/lucapaone76/onedrive-connect)

## Changelog

### Version 0.1.0 (2026-01-17)

**Initial Release - Published to PyPI**

#### Core Features
- `OneDriveClient`: Low-level API access to Microsoft Graph API
- `OneDriveSkill`: LLM-friendly skill interface with safety features
- User confirmation for destructive operations
- Skill metadata for LLM discovery
- Comprehensive type hints and documentation
- Safety features and cancellation support

#### Authentication
- `auth_helper.py`: Interactive authentication script
  - Guides users through Azure AD app setup
  - Browser-based OAuth2 flow
  - Automatic token generation and storage
  - Support for access and refresh tokens
- Multiple authentication methods supported
- Token refresh capability for long-running applications
- Secure token management via environment variables

#### Installation & Distribution
- Published to PyPI: https://pypi.org/project/onedrive-skill/
- Multiple installation options:
  - Core: `pip install onedrive-skill`
  - With auth tools: `pip install onedrive-skill[auth]`
  - With dev tools: `pip install onedrive-skill[dev]`
- Comprehensive documentation for personal OneDrive accounts

#### LLM Integration
- Claude integration guide
- Example prompts for natural language usage
- Metadata API for capability discovery
- Safety level categorization (read-only, write, destructive)

#### Documentation
- Complete skill specification (SKILL.md)
- Detailed README with step-by-step guides
- Azure AD setup instructions for personal accounts
- Requirements documentation (REQUIREMENTS.md)
- Changelog (CHANGELOG.md)
- .env.example template
- Skill manifest JSON for machine-readable metadata

#### Developer Experience
- Full type hints for IDE support
- Comprehensive docstrings
- Example usage scripts
- Development dependencies included
- Testing framework setup

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Compliance

This skill follows LLM agent skills best practices:

- ✅ Structured metadata for LLM discovery
- ✅ Clear safety level categorization
- ✅ User consent for destructive operations
- ✅ Type-safe APIs with full type hints
- ✅ Comprehensive documentation
- ✅ Secure token handling
- ✅ Error handling and validation
