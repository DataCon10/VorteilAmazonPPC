import pytest
import requests
import sys
import os
# Insert the project root (one level up) into sys.path before other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
import pytest
import requests
from scripts.fetch_data import AmazonAdsClient

# DummyResponse is a helper class to mimic the Response object from requests.
class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)
    def json(self):
        return self._json

# Test for get_access_token() success
def test_get_access_token_success(monkeypatch):
    def dummy_post(url, data):
        return DummyResponse({
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token"
        }, 200)
    monkeypatch.setattr(requests, "post", dummy_post)
    
    client = AmazonAdsClient()
    token = client.get_access_token()
    assert token == "dummy_access_token"

# Test for get_profiles() success
def test_get_profiles_success(monkeypatch):
    dummy_profiles = [{"profileId": "123", "countryCode": "GB"}]
    def dummy_get(url, headers):
        return DummyResponse(dummy_profiles, 200)
    monkeypatch.setattr(requests, "get", dummy_get)
    
    client = AmazonAdsClient()
    # Manually set a dummy token for testing purposes.
    client.token = "dummy_access_token"
    profiles = client.get_profiles()
    assert profiles == dummy_profiles

# Test for get_uk_profile_id() when UK profile is found
def test_get_uk_profile_id_found():
    profiles = [
        {"profileId": "123", "countryCode": "GB"},
        {"profileId": "456", "countryCode": "US"}
    ]
    client = AmazonAdsClient()
    uk_profile = client.get_uk_profile_id(profiles)
    assert uk_profile == "123"

# Test for get_uk_profile_id() when no UK profile is found
def test_get_uk_profile_id_not_found():
    profiles = [
        {"profileId": "456", "countryCode": "US"}
    ]
    client = AmazonAdsClient()
    uk_profile = client.get_uk_profile_id(profiles)
    assert uk_profile == ""

# Test for fetch_campaigns() success
def test_fetch_campaigns_success(monkeypatch):
    dummy_campaigns = {"campaigns": [{"id": "camp1"}]}
    def dummy_get(url, headers):
        return DummyResponse(dummy_campaigns, 200)
    monkeypatch.setattr(requests, "get", dummy_get)
    
    client = AmazonAdsClient()
    client.token = "dummy_access_token"
    # Pass a dummy profile id, e.g., "123"
    campaigns = client.fetch_campaigns("123")
    assert campaigns == dummy_campaigns

# Test for fetch_campaigns() failure
def test_fetch_campaigns_failure(monkeypatch):
    def dummy_get(url, headers):
        return DummyResponse({"error": "not found"}, 404)
    monkeypatch.setattr(requests, "get", dummy_get)
    
    client = AmazonAdsClient()
    client.token = "dummy_access_token"
    campaigns = client.fetch_campaigns("123")
    # Since our method returns {} on error, we expect an empty dict.
    assert campaigns == {}
