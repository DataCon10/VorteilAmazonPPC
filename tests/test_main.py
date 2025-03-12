import pytest
import requests
import sys
import os
import importlib


# Fixture to set up test environment variables and reload the module.
@pytest.fixture
def test_env(monkeypatch):

    # Set test environment variables.
    monkeypatch.setenv("AMAZON_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("AMAZON_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setenv("AMAZON_REFRESH_TOKEN", "test_refresh_token")
    monkeypatch.setenv("AMAZON_REDIRECT_URI", "http://localhost:5000/callback")
    monkeypatch.setenv("MARKETPLACE", "EU")
    
    # Ensure the module is reloaded so it picks up the new env variables.
    import vorteilamazonppc.scripts.fetch_data as fetch_data_module
    importlib.reload(fetch_data_module)
    return fetch_data_module


# Fixture that returns an instance of AmazonAdsClient using the test environment.
@pytest.fixture
def amazon_ads_client(test_env):
    from vorteilamazonppc.scripts.fetch_data import AmazonAdsClient
    return AmazonAdsClient()


def test_amazon_ads_client_setup(amazon_ads_client):
    # Using the fixture, we get a client instance with test configuration.
    client = amazon_ads_client
    assert client.client_id == "test_client_id"
    assert client.client_secret == "test_client_secret"
    assert client.refresh_token == "test_refresh_token"
    assert client.redirect_uri == "http://localhost:5000/callback"
    # Optionally, check endpoint values:
    assert "amazon.com" in client.token_url or "amazon.co.uk" in client.token_url
