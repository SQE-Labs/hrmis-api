"""Announcements API client for handling all announcement operations"""
import os
from playwright.sync_api import APIRequestContext
from src.endpoints.announcements import (
    ANNOUNCEMENTS_BASE, 
    ANNOUNCEMENTS_UPDATE,
    ANNOUNCEMENTS_DASHBOARD_LIST,
    announcement_by_id,
    announcements_list
)

class AnnouncementsClient:
    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context
        
    def _p(self, path: str) -> str:
        """Prefix helper: API_PREFIX is the app path."""
        prefix = os.getenv("API_PREFIX", "HRMBackendTest").strip("/")
        return f"/{prefix}/{path.lstrip('/')}"
        
    def get_dashboard_list(self):
        """Get announcements dashboard list"""
        return self.api_context.get(self._p(ANNOUNCEMENTS_DASHBOARD_LIST))
        
    def create_announcement(self, multipart_data: dict):
        """Create new announcement with multipart form data"""
        return self.api_context.put(
            self._p(ANNOUNCEMENTS_BASE),
            multipart=multipart_data
        )
    
    def update_announcement(self, data: dict):
        """Update existing announcement"""
        return self.api_context.put(
            self._p(ANNOUNCEMENTS_UPDATE),
            multipart=data
        )
    
    def get_announcements(self, page_size=10, page=1, status="PENDING"):
        """Get announcements with pagination and status filter"""
        return self.api_context.get(
            self._p(announcements_list(page_size, page, status))
        )
    
    def delete_announcement(self, announcement_id: str):
        """Delete announcement by ID"""
        return self.api_context.delete(
            self._p(announcement_by_id(announcement_id))
        )
