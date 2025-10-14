# src/endpoints/announcements.py
"""Announcement module endpoint constants"""

# Dashboard endpoints
ANNOUNCEMENTS_DASHBOARD_LIST = "announcement"

# Base endpoints
ANNOUNCEMENTS_BASE = "announcement"
ANNOUNCEMENTS_UPDATE = "announcement/update"

# Dynamic endpoints
def announcement_by_id(announcement_id):
    return f"{ANNOUNCEMENTS_BASE}/{announcement_id}"

# Query parameter helpers
def announcements_list(page_size=10, page=1, status="PENDING"):
    return f"{ANNOUNCEMENTS_BASE}?pageSize={page_size}&page={page}&status={status}"
