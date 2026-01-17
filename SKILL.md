# OneDrive Connect Skill

## Skill Information

**Name**: onedrive-connect  
**Version**: 0.1.0  
**Author**: lucapaone76  
**License**: MIT  
**Category**: File Management, Cloud Storage  
**Tags**: onedrive, microsoft, graph-api, cloud, storage, files

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

**Type**: OAuth2 Bearer Token  
**Provider**: Microsoft Graph API  
**Required Scopes**:
- `Files.ReadWrite` or `Files.ReadWrite.All`
- `User.Read`

**Environment Variable**: `ONEDRIVE_ACCESS_TOKEN`

## Installation

```bash
pip install -r requirements.txt
```

Or for development:

```bash
pip install -e .
```

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

### Required Environment Variables

- `ONEDRIVE_ACCESS_TOKEN`: OAuth2 access token for Microsoft Graph API

### Optional Environment Variables

- `ONEDRIVE_API_BASE_URL`: Custom API endpoint (default: `https://graph.microsoft.com/v1.0`)

### Configuration Example

```bash
export ONEDRIVE_ACCESS_TOKEN="your_access_token_here"
```

Or using a `.env` file with python-dotenv:

```bash
ONEDRIVE_ACCESS_TOKEN=your_access_token_here
```

## Dependencies

### Core Dependencies

- `requests>=2.31.0`: HTTP library for Microsoft Graph API calls

### Optional Dependencies

- `msal>=1.20.0`: Microsoft Authentication Library for token generation
- `python-dotenv>=1.0.0`: Load environment variables from .env file

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

Initial release with:
- OneDriveClient for low-level API access
- OneDriveSkill for LLM-friendly operations
- User confirmation for destructive operations
- Skill metadata for LLM discovery
- Comprehensive documentation
- Safety features and cancellation support

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
