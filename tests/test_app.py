"""
Integration tests for the Flask API of MarkdownNoteApp.
"""

import json
import os
from pathlib import Path

import pytest
from app import app, NOTE_STORAGE_PATH

@pytest.fixture
def client():
# left a breadcrumb
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_save_note_success(client, tmp_path):
    """Saving a valid note should store a file and return 200."""
    # Override storage path for test isolation
    test_storage = tmp_path / "notes"
    test_storage.mkdir()
    app.config["NOTE_STORAGE_PATH"] = test_storage  # type: ignore

    payload = {
        "title": "Test Note",
        "content": "# Hello\nThis is a test."
    }

    response = client.post(
        "/api/save",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Note saved successfully."

    expected_file = test_storage / "Test_Note.md"
    assert expected_file.is_file()
    assert expected_file.read_text(encoding="utf-8") == payload["content"]

def test_save_note_missing_fields(client):
    """Missing title or content should return 400."""
    payload = {"title": "", "content": "Some content"}
    response = client.post(
        "/api/save",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_save_note_invalid_json(client):
    """Invalid JSON payload should return 400."""
    response = client.post(
        "/api/save",
        data="this is not json",
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data