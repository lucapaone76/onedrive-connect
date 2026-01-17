"""OneDrive Skill - A Python skill for connecting to Microsoft OneDrive.

This package provides a skill interface for LLMs to interact with OneDrive
using the Microsoft Graph API. Authentication tokens must be provided via
environment variables or secrets.
"""

from .onedrive_client import OneDriveClient, OneDriveSkill

__version__ = "0.1.0"
__all__ = ["OneDriveClient", "OneDriveSkill"]
