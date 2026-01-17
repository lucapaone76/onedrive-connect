"""OneDrive Client implementation using Microsoft Graph API."""

import os
from typing import Dict, List, Optional, Any
import requests


class OneDriveClient:
    """Client for interacting with Microsoft OneDrive via Graph API.
    
    This client uses the Microsoft Graph API to perform operations on OneDrive.
    Authentication is handled via access tokens that should be provided through
    environment variables or secure secret management systems.
    
    Required environment variables:
        ONEDRIVE_ACCESS_TOKEN: OAuth2 access token for Microsoft Graph API
    
    Optional environment variables:
        ONEDRIVE_API_BASE_URL: Base URL for Microsoft Graph API 
                               (default: https://graph.microsoft.com/v1.0)
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize OneDrive client.
        
        Args:
            access_token: OAuth2 access token. If not provided, will attempt
                         to read from ONEDRIVE_ACCESS_TOKEN environment variable.
        
        Raises:
            ValueError: If no access token is provided or found in environment.
        """
        self.access_token = access_token or os.getenv("ONEDRIVE_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError(
                "No access token provided. Either pass access_token parameter "
                "or set ONEDRIVE_ACCESS_TOKEN environment variable."
            )
        
        self.api_base_url = os.getenv(
            "ONEDRIVE_API_BASE_URL", 
            "https://graph.microsoft.com/v1.0"
        )
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Microsoft Graph API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests
        
        Returns:
            JSON response from the API
        
        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        url = f"{self.api_base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            **kwargs
        )
        response.raise_for_status()
        
        # Some responses (like DELETE) may not have content
        if response.status_code == 204 or not response.content:
            return {}
        
        return response.json()
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get information about the authenticated user.
        
        Returns:
            Dictionary containing user information
        """
        return self._make_request("GET", "/me")
    
    def list_root_items(self) -> List[Dict[str, Any]]:
        """List items in the root of the user's OneDrive.
        
        Returns:
            List of items (files and folders) in the root directory
        """
        response = self._make_request("GET", "/me/drive/root/children")
        return response.get("value", [])
    
    def list_items(self, folder_path: str = "") -> List[Dict[str, Any]]:
        """List items in a specific folder.
        
        Args:
            folder_path: Path to the folder (e.g., "Documents/MyFolder")
                        If empty, lists root items.
        
        Returns:
            List of items in the specified folder
        """
        if not folder_path:
            return self.list_root_items()
        
        endpoint = f"/me/drive/root:/{folder_path}:/children"
        response = self._make_request("GET", endpoint)
        return response.get("value", [])
    
    def get_item_info(self, item_id: str) -> Dict[str, Any]:
        """Get information about a specific item.
        
        Args:
            item_id: The ID of the item
        
        Returns:
            Dictionary containing item information
        """
        return self._make_request("GET", f"/me/drive/items/{item_id}")
    
    def download_file(self, item_id: str) -> bytes:
        """Download a file from OneDrive.
        
        Args:
            item_id: The ID of the file to download
        
        Returns:
            File content as bytes
        """
        endpoint = f"/me/drive/items/{item_id}/content"
        url = f"{self.api_base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content
    
    def upload_file(
        self, 
        file_path: str, 
        content: bytes, 
        overwrite: bool = True
    ) -> Dict[str, Any]:
        """Upload a file to OneDrive.
        
        Args:
            file_path: Path where to upload the file (e.g., "Documents/myfile.txt")
            content: File content as bytes
            overwrite: Whether to overwrite existing file
        
        Returns:
            Dictionary containing information about the uploaded file
        """
        endpoint = f"/me/drive/root:/{file_path}:/content"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"
        
        url = f"{self.api_base_url}{endpoint}"
        response = requests.put(url, headers=headers, data=content)
        response.raise_for_status()
        return response.json()
    
    def create_folder(self, folder_name: str, parent_path: str = "") -> Dict[str, Any]:
        """Create a new folder in OneDrive.
        
        Args:
            folder_name: Name of the folder to create
            parent_path: Path to parent folder (empty for root)
        
        Returns:
            Dictionary containing information about the created folder
        """
        if parent_path:
            endpoint = f"/me/drive/root:/{parent_path}:/children"
        else:
            endpoint = "/me/drive/root/children"
        
        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        
        return self._make_request("POST", endpoint, json=data)
    
    def delete_item(self, item_id: str) -> None:
        """Delete an item from OneDrive.
        
        Args:
            item_id: The ID of the item to delete
        """
        self._make_request("DELETE", f"/me/drive/items/{item_id}")
    
    def search_items(self, query: str) -> List[Dict[str, Any]]:
        """Search for items in OneDrive.
        
        Args:
            query: Search query string
        
        Returns:
            List of items matching the search query
        """
        endpoint = f"/me/drive/root/search(q='{query}')"
        response = self._make_request("GET", endpoint)
        return response.get("value", [])


class OneDriveSkill:
    """Skill wrapper for OneDrive operations.
    
    This class provides a simplified interface for common OneDrive operations
    that can be easily integrated with LLM systems.
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize OneDrive skill.
        
        Args:
            access_token: OAuth2 access token. If not provided, will attempt
                         to read from ONEDRIVE_ACCESS_TOKEN environment variable.
        """
        self.client = OneDriveClient(access_token=access_token)
    
    def list_files(self, folder_path: str = "") -> str:
        """List files in a folder (skill-friendly output).
        
        Args:
            folder_path: Path to the folder (empty for root)
        
        Returns:
            Formatted string with file listing
        """
        items = self.client.list_items(folder_path)
        if not items:
            return "No items found in the specified folder."
        
        result = []
        for item in items:
            item_type = "Folder" if "folder" in item else "File"
            name = item.get("name", "Unknown")
            size = item.get("size", 0)
            result.append(f"- [{item_type}] {name} ({size} bytes)")
        
        return "\n".join(result)
    
    def get_file_content(self, item_id: str) -> bytes:
        """Get file content by item ID.
        
        Args:
            item_id: The ID of the file
        
        Returns:
            File content as bytes
        """
        return self.client.download_file(item_id)
    
    def upload_content(self, file_path: str, content: bytes) -> str:
        """Upload content to OneDrive.
        
        Args:
            file_path: Path where to upload the file
            content: File content as bytes
        
        Returns:
            Success message with file information
        """
        result = self.client.upload_file(file_path, content)
        return f"File uploaded successfully: {result.get('name')} (ID: {result.get('id')})"
    
    def search(self, query: str) -> str:
        """Search for items in OneDrive.
        
        Args:
            query: Search query string
        
        Returns:
            Formatted string with search results
        """
        items = self.client.search_items(query)
        if not items:
            return f"No items found matching '{query}'."
        
        result = [f"Found {len(items)} item(s):"]
        for item in items[:10]:  # Limit to 10 results
            item_type = "Folder" if "folder" in item else "File"
            name = item.get("name", "Unknown")
            result.append(f"- [{item_type}] {name} (ID: {item.get('id')})")
        
        if len(items) > 10:
            result.append(f"... and {len(items) - 10} more items")
        
        return "\n".join(result)
