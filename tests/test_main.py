import pytest
import requests
from scripts.fetch_data import get_access_token, get_profiles, get_uk_profile_id, fetch_campaigns

# TEST NOTE: DummyResponse is a helper class to mimic the Response object from requests.
class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)
    def json(self):
        return self._json

# Test for get_access_token() when successful
def test_get_access_token_success(monkeypatch):
    # TEST NOTE: Dummy POST response with a dummy access token and refresh token.
    def dummy_post(url, data):
        return DummyResponse({"access_token": "dummy_access_token", "refresh_token": "dummy_refresh_token"}, 200)
    
    monkeypatch.setattr(requests, "post", dummy_post)
    token = get_access_token()
    assert token == "dummy_access_token"

# Test for get_access_token() when token exchange fails
def test_get_access_token_failure(monkeypatch):
    def dummy_post(url, data):
        return DummyResponse({"error": "invalid_request"}, 400)
    monkeypatch.setattr(requests, "post", dummy_post)
    token = get_access_token()
    assert token is None

# Test for get_profiles() when successful
def test_get_profiles_success(monkeypatch):
    dummy_profiles = [{"profileId": "123", "countryCode": "GB"}]
    def dummy_get(url, headers):
        return DummyResponse(dummy_profiles, 200)
    monkeypatch.setattr(requests, "get", dummy_get)
    profiles = get_profiles("dummy_access_token")
    assert profiles == dummy_profiles

# Test for get_uk_profile_id() when UK profile is found
def test_get_uk_profile_id_found():
    profiles = [
        {"profileId": "123", "countryCode": "GB"},
        {"profileId": "456", "countryCode": "US"}
    ]
    uk_profile = get_uk_profile_id(profiles)
    assert uk_profile == "123"

# Test for get_uk_profile_id() when no UK profile is found
def test_get_uk_profile_id_not_found():
    profiles = [
        {"profileId": "456", "countryCode": "US"}
    ]
    uk_profile = get_uk_profile_id(profiles)
    assert uk_profile is None

# Test for fetch_campaigns() when campaigns are returned successfully
def test_fetch_campaigns_success(monkeypatch):
    dummy_campaigns = {"campaigns": [{"id": "camp1"}]}
    def dummy_get(url, headers):
        return DummyResponse(dummy_campaigns, 200)
    monkeypatch.setattr(requests, "get", dummy_get)
    campaigns = fetch_campaigns("dummy_access_token", "123")
    assert campaigns == dummy_campaigns

# Test for fetch_campaigns() when campaign retrieval fails
def test_fetch_campaigns_failure(monkeypatch):
    def dummy_get(url, headers):
        return DummyResponse({"error": "not found"}, 404)
    monkeypatch.setattr(requests, "get", dummy_get)
    campaigns = fetch_campaigns("dummy_access_token", "123")
    assert campaigns is None
