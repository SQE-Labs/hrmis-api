import pytest
from src.clients.announcements_client import AnnouncementsClient

# ANN-002: Missing mandatory field
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 201 instead of 400 for missing title")
def test_create_announcement_missing_title(ctx, sample_announcement_file):
    client = AnnouncementsClient(ctx)
    payload = {
        'description': 'desc',
        'eventType': 'Classroom Session',
        'presentedBy': 'Rollins',
        'startDateTime': '2025-06-06T10:30:00',
        'endDateTime': '2025-06-06T12:30:00',
        'venue': 'Cabin 02',
        'mode': 'Offline',
        'file': sample_announcement_file
    }
    res = client.create_announcement(payload)
    assert res.status == 400, f"Expected 400, got {res.status}"

# ANN-003: Invalid date range
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 201 instead of 400 for invalid date")
def test_create_announcement_invalid_date(ctx, invalid_date_announcement_data, sample_announcement_file):
    client = AnnouncementsClient(ctx)
    payload = {**invalid_date_announcement_data, 'file': sample_announcement_file}
    res = client.create_announcement(payload)
    assert res.status == 400

# ANN-004: Invalid file type
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 201 instead of 415")
def test_create_announcement_invalid_file_type(ctx, valid_announcement_data, invalid_announcement_file):
    client = AnnouncementsClient(ctx)
    payload = {**valid_announcement_data, 'file': invalid_announcement_file}
    res = client.create_announcement(payload)
    assert res.status == 415

# ANN-007: Missing ID in update
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 500 instead of 400 when ID is missing in update")
def test_update_announcement_missing_id(ctx, valid_announcement_data):
    client = AnnouncementsClient(ctx)
    payload = {**valid_announcement_data}
    res = client.update_announcement(payload)
    assert res.status == 400, f"Expected 400, got {res.status}"

# ANN-008: Invalid ID in update
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 401 instead of 404 for invalid ID")
def test_update_announcement_invalid_id(ctx, valid_announcement_data):
    client = AnnouncementsClient(ctx)
    payload = {"id": 999999, **valid_announcement_data}
    res = client.update_announcement(payload)
    assert res.status == 404

# ANN-018: Malformed delete request
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Bug: API returns 401 instead of 400 for malformed ID")
def test_delete_announcement_malformed_request(ctx):
    client = AnnouncementsClient(ctx)
    res = client.delete_announcement("")
    assert res.status == 400
    
# ANN-012: Invalid query params
@pytest.mark.negative
@pytest.mark.module_announcements
@pytest.mark.xfail(reason="Backend may not validate query params")
def test_pagination_invalid_query_params(ctx):
    client = AnnouncementsClient(ctx)
    response = client.get_announcements(page_size=-1, page=-1, status="INVALID")
    assert response.status == 400, f"Expected 400, got {response.status}"
