# Requirements and Dependencies

This document outlines all requirements, dependencies, and system prerequisites for the OneDrive Connect skill.

## Table of Contents

- [System Requirements](#system-requirements)
- [Python Version](#python-version)
- [Core Dependencies](#core-dependencies)
- [Development Dependencies](#development-dependencies)
- [Authentication Requirements](#authentication-requirements)
- [Platform-Specific Notes](#platform-specific-notes)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Hardware Requirements

- **CPU**: Any modern processor (x86_64 or ARM64)
- **RAM**: 512 MB minimum, 1 GB recommended
- **Storage**: 50 MB free disk space
- **Network**: Internet connection for accessing Microsoft Graph API

### Operating Systems

The OneDrive Connect skill is tested and supported on:

- **Linux**: Ubuntu 20.04+, Debian 10+, CentOS 7+, Fedora 30+
- **macOS**: macOS 10.15 (Catalina) or later
- **Windows**: Windows 10, Windows 11, Windows Server 2016+

## Python Version

### Required Python Version

- **Minimum**: Python 3.8
- **Recommended**: Python 3.11 or later
- **Maximum tested**: Python 3.12

### Version Check

Verify your Python version:

```bash
python --version
# or
python3 --version
```

If you need to install or upgrade Python:

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```

- **macOS** (using Homebrew):
  ```bash
  brew install python@3.11
  ```

- **Windows**: Download from [python.org](https://www.python.org/downloads/)

## Core Dependencies

These dependencies are required for the skill to function:

### Production Dependencies

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| `requests` | >=2.31.0 | HTTP library for Microsoft Graph API calls | Apache 2.0 |

### Installation

Install core dependencies:

```bash
pip install -r requirements.txt
```

Content of `requirements.txt`:
```
requests>=2.31.0
```

### Dependency Details

#### requests (>=2.31.0)

- **Purpose**: Makes HTTP requests to Microsoft Graph API
- **Why this version**: Version 2.31.0+ includes security fixes for CVE-2023-32681
- **Key features used**:
  - HTTP methods (GET, POST, PUT, DELETE)
  - Request headers and authentication
  - Response parsing
  - Error handling
- **Documentation**: https://docs.python-requests.org/

## Development Dependencies

These dependencies are only needed for development, testing, and code quality:

### Development Tools

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=7.0.0 | Testing framework |
| `pytest-cov` | >=4.0.0 | Code coverage reporting |
| `black` | >=23.0.0 | Code formatter |
| `ruff` | >=0.1.0 | Fast Python linter |

### Installation

Install with development dependencies:

```bash
pip install -e ".[dev]"
```

Or from pyproject.toml:

```bash
pip install pytest>=7.0.0 pytest-cov>=4.0.0 black>=23.0.0 ruff>=0.1.0
```

### Development Tool Usage

**Run tests:**
```bash
pytest
```

**Code coverage:**
```bash
pytest --cov=onedrive_skill --cov-report=html
```

**Format code:**
```bash
black onedrive_skill/
```

**Lint code:**
```bash
ruff check onedrive_skill/
```

## Authentication Requirements

### Microsoft Azure Active Directory

To use this skill, you need:

1. **Azure AD Application Registration**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Create an app registration
   - Note your Application (client) ID

2. **Microsoft Graph API Permissions**
   - Delegated permissions required:
     - `Files.ReadWrite` or `Files.ReadWrite.All`
     - `User.Read`
   - Admin consent may be required depending on your organization

3. **OAuth2 Access Token**
   - Generate using one of these flows:
     - Authorization Code Flow (web apps)
     - Device Code Flow (CLI/desktop apps)
     - Interactive Flow (using MSAL)
   
   **Optional dependency for token generation:**
   ```bash
   pip install msal>=1.20.0
   ```

### Environment Variables

The skill requires the following environment variable:

```bash
export ONEDRIVE_ACCESS_TOKEN="your_access_token_here"
```

Optional environment variables:

```bash
# Custom API endpoint (default: https://graph.microsoft.com/v1.0)
export ONEDRIVE_API_BASE_URL="https://graph.microsoft.com/v1.0"
```

## Platform-Specific Notes

### Linux

**Ubuntu/Debian:**
- Ensure `python3-pip` is installed: `sudo apt install python3-pip`
- May need `python3-venv`: `sudo apt install python3-venv`

**CentOS/RHEL:**
- Use `python3` and `pip3` explicitly
- May need EPEL repository for latest Python versions

### macOS

- Use Homebrew for easiest Python management
- Xcode Command Line Tools may be required:
  ```bash
  xcode-select --install
  ```

### Windows

- Use PowerShell or Command Prompt
- Path separators in code use forward slashes (/) - the skill handles this automatically
- Environment variables are set differently:
  ```powershell
  $env:ONEDRIVE_ACCESS_TOKEN="your_token"
  ```

## Optional Dependencies

### For Enhanced Authentication (MSAL)

If you want to use MSAL for token generation:

```bash
pip install msal>=1.20.0
```

Example usage:
```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="YOUR_CLIENT_ID",
    authority="https://login.microsoftonline.com/common"
)

result = app.acquire_token_interactive(
    scopes=["Files.ReadWrite", "User.Read"]
)
```

### For .env File Support

If you want to load environment variables from a `.env` file:

```bash
pip install python-dotenv>=1.0.0
```

Usage:
```python
from dotenv import load_dotenv
load_dotenv()

from onedrive_skill import OneDriveSkill
skill = OneDriveSkill()  # Reads from .env file
```

## Security Considerations

### Dependency Security

- All dependencies are pinned to minimum versions with known security fixes
- `requests>=2.31.0` addresses CVE-2023-32681
- Regularly update dependencies: `pip install --upgrade -r requirements.txt`

### Best Practices

1. **Use virtual environments** to isolate dependencies
2. **Never commit** `.env` files or tokens to version control
3. **Rotate tokens regularly** - access tokens expire
4. **Use least privilege** - only request necessary API permissions
5. **Monitor dependencies** for security advisories

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests>=2.31.0
```

#### "ImportError: cannot import name 'OneDriveSkill'"

**Solution:**
Ensure you're in the correct directory and the package is installed:
```bash
pip install -e .
```

#### "ValueError: No access token provided"

**Solution:**
Set the environment variable:
```bash
export ONEDRIVE_ACCESS_TOKEN="your_token"
```

#### SSL Certificate Errors

**Solution:**
Update certifi package:
```bash
pip install --upgrade certifi
```

#### Permission Denied on Linux/Mac

**Solution:**
Use `--user` flag or virtual environment:
```bash
pip install --user -r requirements.txt
```

### Dependency Conflicts

If you encounter dependency conflicts:

1. **Use a fresh virtual environment:**
   ```bash
   python -m venv fresh_env
   source fresh_env/bin/activate  # On Windows: fresh_env\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Check for conflicting packages:**
   ```bash
   pip check
   ```

3. **Use pip-tools for dependency resolution:**
   ```bash
   pip install pip-tools
   pip-compile requirements.txt
   ```

## Version Compatibility Matrix

| OneDrive Skill | Python | requests | pytest | Status |
|---------------|--------|----------|--------|--------|
| 0.1.0 | 3.8-3.12 | >=2.31.0 | >=7.0.0 | Current |

## Upgrading

### From requirements.txt to pyproject.toml

If you've been using `requirements.txt`, you can now use `pyproject.toml`:

```bash
pip install -e .
```

This reads dependencies from `pyproject.toml` automatically.

### Upgrading Dependencies

To upgrade all dependencies to latest versions:

```bash
pip install --upgrade -r requirements.txt
```

To upgrade specific packages:

```bash
pip install --upgrade requests
```

## Getting Help

If you encounter issues not covered here:

1. Check the [main README](README.md) for usage examples
2. Review the [skill manifest](skill_manifest.json) for capability details
3. Open an issue at [GitHub Issues](https://github.com/lucapaone76/onedrive-connect/issues)

## License

All dependencies are open source with compatible licenses:
- requests: Apache License 2.0
- pytest: MIT License
- black: MIT License
- ruff: MIT License

This project itself is licensed under MIT License - see [LICENSE](LICENSE) file.
