import sys
import os
import pytest
import importlib

@pytest.fixture(autouse=True)
def reset_test_env(monkeypatch):
    """
    Reset and set environment variables for tests, then reload modules so that 
    the test values are used instead of the ones from .env.
    """
    # Remove pre-existing environment variables
    for var in [
        "AMAZON_CLIENT_ID", 
        "AMAZON_CLIENT_SECRET", 
        "AMAZON_REFRESH_TOKEN", 
        "AMAZON_REDIRECT_URI", 
        "MARKETPLACE", 
        "TOKEN_URL", 
        "CAMPAIGNS_ENDPOINT", 
        "PROFILES_ENDPOINT"
    ]:
        monkeypatch.delenv(var, raising=False)
    
    # Set test-specific values
    monkeypatch.setenv("AMAZON_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("AMAZON_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setenv("AMAZON_REFRESH_TOKEN", "test_refresh_token")
    monkeypatch.setenv("AMAZON_REDIRECT_URI", "http://localhost:5000/callback")
    monkeypatch.setenv("MARKETPLACE", "EU")
    # Optionally override other config variables here if needed.

    # # Insert the project root into sys.path (if not already set)
    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # if project_root not in sys.path:
    #     sys.path.insert(0, project_root)
    
    # Reload modules that depend on environment variables
    import vorteilamazonppc.scripts.fetch_data as fetch_data_module
    importlib.reload(fetch_data_module)
