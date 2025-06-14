import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def set_test_environment(monkeypatch):
    """
    Set environment variables for the entire test session.
    This fixture runs automatically for all tests.
    """
    monkeypatch.setenv("ENABLE_BQML", "false")
    monkeypatch.setenv("ENABLE_GOOGLE_SEARCH", "false") 