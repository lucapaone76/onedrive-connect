# Changelog

All notable changes to the OneDrive Connect skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-01-17

### Added

#### Authentication
- **`auth_helper.py`** - Interactive authentication script for easy token generation
  - Guides users through Azure AD app registration
  - Opens browser for Microsoft OAuth2 authentication
  - Automatically generates access and refresh tokens
  - Saves tokens to `.env` file with user confirmation
  - Includes comprehensive setup instructions and security reminders
- **Package extras for authentication**: `pip install onedrive-skill[auth]`
  - Includes `msal>=1.20.0` for Microsoft Authentication Library
  - Includes `python-dotenv>=1.0.0` for .env file support
- **`requirements-auth.txt`** - Standalone authentication dependencies file
- Token refresh documentation and examples in README and SKILL.md

#### Documentation
- **Comprehensive Claude integration guide** in README.md
  - Step-by-step setup for Claude.ai and Claude Code CLI
  - Example prompts for natural language usage
  - Security considerations for Claude usage
  - Quick start guide (3 steps to get started)
- **Detailed Azure AD authentication setup** for personal Microsoft accounts
  - Screenshot-level detail for Azure Portal navigation
  - Step-by-step app registration instructions
  - API permissions configuration guide
  - Two authentication methods (helper script and manual)
- **Enhanced SKILL.md** with authentication section
  - Quick reference section with PyPI link
  - "Using with Claude and LLM Systems" section
  - Comprehensive configuration methods
  - Token management and refresh documentation
  - All environment variables documented
- **Enhanced `.env.example`** template
  - Added `ONEDRIVE_REFRESH_TOKEN` variable
  - Added `AZURE_CLIENT_ID` variable
  - Comprehensive comments for all variables
  - Usage instructions included

#### Installation
- **Published to PyPI**: https://pypi.org/project/onedrive-skill/
  - Package available via `pip install onedrive-skill`
  - Multiple installation options (core, auth, dev)
- **Installation extras** in setup.cfg
  - `[auth]` extra for authentication tools
  - `[dev]` extra for development tools

### Changed
- Updated README.md with PyPI installation as Method 2
- Enhanced authentication setup instructions with more detail
- Improved documentation structure with better navigation
- Updated SKILL.md changelog with detailed feature breakdown

### Documentation Improvements
- Added platform-specific environment variable setup (Linux/Mac/Windows)
- Multiple configuration methods documented (.env, environment variables, direct)
- Token expiration and refresh token usage explained
- Security best practices for token handling
- Example Claude prompts and use cases

## [0.1.0] - 2026-01-17

### Added

#### Core Functionality
- Initial implementation of `OneDriveClient` class for Microsoft Graph API integration
- `OneDriveSkill` class providing LLM-friendly wrapper with formatted string outputs
- Support for 9 OneDrive operations: list, search, download, upload, create folder, delete

#### Safety Features
- User confirmation mechanism for destructive operations
- Customizable confirmation callback for UI/LLM system integration
- Default console-based confirmation handler
- Clear warning messages for destructive operations (⚠️ DESTRUCTIVE OPERATION ⚠️)
- Cancellation support for all confirmation-required operations

#### Methods - Read Operations (Safe)
- `list_files(folder_path)` - List files and folders in a directory
- `search(query)` - Search for files across OneDrive
- `get_file_content(item_id)` - Download file content
- `get_user_info()` - Get authenticated user information
- `get_item_info(item_id)` - Get item metadata

#### Methods - Write Operations
- `create_folder(folder_name, parent_path, conflict_behavior)` - Create folders with configurable conflict resolution
- `upload_content(file_path, content, require_confirmation)` - Upload files with optional confirmation

#### Methods - Destructive Operations (Mandatory Confirmation)
- `delete_item(item_id, item_name, require_confirmation)` - Delete files/folders with mandatory confirmation

#### Skill Discovery
- `get_skill_metadata()` - Returns skill capabilities and safety information
- `skill_manifest.json` - Structured skill definitions with parameters and safety levels
- `SKILL_METADATA` export at package level

#### Security
- Environment variable-based authentication (`ONEDRIVE_ACCESS_TOKEN`)
- No hardcoded secrets or credentials
- URL encoding for all user-provided inputs (paths, queries)
- Secure dependency: `requests>=2.31.0` (addresses CVE-2023-32681)
- Centralized request handling with proper error handling

#### Documentation
- Comprehensive README.md with installation guide and usage examples
- REQUIREMENTS.md with detailed dependency and system requirements
- SKILL.md with complete API reference and skill specification
- CHANGELOG.md for version history tracking
- Inline docstrings for all public methods
- Type hints throughout the codebase
- Example usage script (`example_usage.py`)

#### Project Configuration
- `pyproject.toml` for Python packaging metadata
- `requirements.txt` for dependency management
- `.env.example` template for configuration
- `.gitignore` properly configured to exclude sensitive files

#### Testing & Quality
- Import validation tests
- Method signature validation
- URL encoding verification
- Confirmation mechanism tests
- CodeQL security scan (0 alerts)

### Security
- All authentication via environment variables (no hardcoded tokens)
- URL encoding with `safe='/'` for paths, `safe=' '` for search queries
- Path handling using `pathlib` for robustness
- Error handling for file operations and JSON parsing
- Passed CodeQL security analysis with zero alerts

### Documentation Standards
- LLM Skills Compliance section explaining best practices adherence
- Quick Links navigation in README
- Platform-specific installation notes (Linux, macOS, Windows)
- Docker installation alternative
- Virtual environment setup instructions
- 5 different installation methods documented
- Troubleshooting guide with 7+ common scenarios
- Version compatibility matrix
- Security considerations and best practices

### Development Tools
- Black code formatter configuration
- Ruff linter configuration
- pytest test framework setup
- pytest-cov for coverage reporting

## [Unreleased]

### Planned Features
- Resumable upload sessions for large files
- Batch operations for multiple files
- Support for shared folders and permissions
- File version history access
- Automatic token refresh mechanism
- Additional test coverage
- Performance optimizations
- Enhanced error messages with recovery suggestions

### Known Limitations
- Large file uploads (>4MB) may timeout without resumable sessions
- No support for shared OneDrive folders yet
- Token refresh must be handled externally
- Rate limiting is handled by the API but not tracked in the client

## Release Notes

### Version 0.1.0 Highlights

This is the initial release of the OneDrive Connect skill, providing a production-ready implementation for LLM systems to interact with Microsoft OneDrive.

**Key Features:**
- ✅ Complete CRUD operations for OneDrive files and folders
- ✅ User safety with confirmation for destructive operations
- ✅ LLM-optimized interface with formatted string outputs
- ✅ Comprehensive documentation and examples
- ✅ Security-first design with no hardcoded credentials
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Type-safe APIs with full type hints

**Security & Compliance:**
- ✅ Zero security vulnerabilities (CodeQL scan passed)
- ✅ Follows LLM agent skills best practices
- ✅ User consent required for destructive operations
- ✅ Clear safety level categorization

**Getting Started:**
See [README.md](README.md) for installation instructions and [SKILL.md](SKILL.md) for complete API reference.

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.1 | 2026-01-17 | Added authentication helper, PyPI publishing, Claude integration guide |
| 0.1.0 | 2026-01-17 | Initial release with core functionality |

---

## Contributing

When contributing to this project, please:

1. Update the `[Unreleased]` section with your changes
2. Follow the changelog format (Added, Changed, Deprecated, Removed, Fixed, Security)
3. Include issue/PR numbers where applicable
4. Update version history table on release

For more information, see [Contributing Guidelines](README.md#contributing).

## Versioning Scheme

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

## Links

- [Repository](https://github.com/lucapaone76/onedrive-connect)
- [Issues](https://github.com/lucapaone76/onedrive-connect/issues)
- [Pull Requests](https://github.com/lucapaone76/onedrive-connect/pulls)
