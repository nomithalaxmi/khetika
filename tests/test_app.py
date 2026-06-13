"""
Tests for Khetika Flask app routes and core logic.
Run with: pytest tests/ -v --cov=. --cov-report=term-missing
"""
import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app
from database import init_db


@pytest.fixture
def client():
    """Flask test client with in-memory DB."""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test_secret"
    with patch("database.DB_PATH", ":memory:"):
        init_db()
        with flask_app.test_client() as client:
            yield client


# ── Route Tests ───────────────────────────────────────────────────────────────

def test_index_returns_200(client):
    """Home page should load successfully."""
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_contains_khetika(client):
    """Home page should contain the brand name."""
    resp = client.get("/")
    assert b"Khetika" in resp.data


def test_chat_empty_message_returns_400(client):
    """Chat endpoint should reject empty message and no image."""
    resp = client.post("/chat", data={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_knowledge_base_returns_200(client):
    """Knowledge base page should load."""
    resp = client.get("/knowledge")
    assert resp.status_code == 200


def test_profile_save_missing_fields(client):
    """Profile save should return 400 if crop or date missing."""
    resp = client.post(
        "/profile/save",
        json={"crop_name": "", "sowing_date": ""},
        content_type="application/json"
    )
    assert resp.status_code == 400


def test_weekly_task_no_profile(client):
    """Weekly task endpoint should return null task if no profile set."""
    resp = client.get("/profile/weekly_task")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["task"] is None


# ── Crop Calendar Tests ───────────────────────────────────────────────────────

def test_crop_calendar_known_crop():
    """Week task lookup for a known crop should return a task."""
    from crop_calendar import get_week_task
    week, task = get_week_task("rice", "2020-01-01")  # far past → capped week
    assert isinstance(week, int)
    assert week >= 1


def test_crop_calendar_unknown_crop():
    """Unknown crop should return a fallback, not crash."""
    from crop_calendar import get_week_task
    week, task = get_week_task("unknowncrop", "2024-01-01")
    assert week is not None


# ── Database Tests ────────────────────────────────────────────────────────────

def test_log_and_retrieve_query():
    """Logging a query should allow it to be retrieved."""
    with patch("database.DB_PATH", ":memory:"):
        from database import init_db, log_query, get_top_queries
        init_db()
        log_query("test question", "test answer", "en")
        rows = get_top_queries(10)
        assert len(rows) >= 1
        assert rows[0][0] == "test question"


def test_save_and_get_farmer_profile():
    """Saving a farmer profile should allow retrieval."""
    with patch("database.DB_PATH", ":memory:"):
        from database import init_db, save_farmer_profile, get_farmer_profile
        init_db()
        save_farmer_profile("sess123", "rice", "2024-06-01", "en")
        profile = get_farmer_profile("sess123")
        assert profile is not None
        assert profile[0] == "rice"
        assert profile[1] == "2024-06-01"


# ── Chat Route (mocked Gemini) ────────────────────────────────────────────────

def test_chat_text_message_calls_gemini(client):
    """Chat with a text message should call Gemini and return a reply."""
    mock_response = MagicMock()
    mock_response.text = "Apply urea fertilizer at 50kg/acre."

    with patch("app.model.generate_content", return_value=mock_response), \
         patch("app.detect_lang", return_value="en"), \
         patch("database.log_query"):
        resp = client.post("/chat", data={"message": "What fertilizer for rice?"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "reply" in data
        assert data["reply"] == "Apply urea fertilizer at 50kg/acre."
        assert data["lang"] == "en"
