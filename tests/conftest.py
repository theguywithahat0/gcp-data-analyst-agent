import pytest
import os

@pytest.fixture(scope="function", autouse=True)
def set_test_environment(monkeypatch):
    """
    Set environment variables for each test function.
    This fixture runs automatically for all tests.
    """
    # Set test environment variables
    # Note: In our simplified framework, BQML is always enabled and search is removed
    pass  # No environment variables needed for our simplified framework 