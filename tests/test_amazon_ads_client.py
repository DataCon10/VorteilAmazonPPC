import pytest
import requests
from vorteilamazonppc.scripts.fetch_data import AmazonAdsClient

# DummyResponse class to simulate requests.Response
class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)
    def json(self):
        return self._json

def test_get_access_token_success(monkeypatch):
    # Define a dummy POST function that returns a successful token response.
    def dummy_post(url, data):
        # Optionally, assert that the payload contains the correct values.
        assert data.get("grant_type") == "refresh_token"
        # Return a DummyResponse with a dummy access token and refresh token.
        return DummyResponse({
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token"
        }, 200)
    
    # Monkeypatch requests.post to use our dummy_post function.
    monkeypatch.setattr(requests, "post", dummy_post)
    
    # Create an instance of the client.
    client = AmazonAdsClient()
    # Call the get_access_token() method.
    token = client.get_access_token()
    
    # Assert that the returned token is as expected.
    assert token == "dummy_access_token"
    # Also, verify that the token was stored in the instance.
    assert client.token == "dummy_access_token"

# Optionally, you can add a failure scenario test as well.
def test_get_access_token_failure(monkeypatch):
    def dummy_post(url, data):
        return DummyResponse({"error": "invalid_request"}, 400)
    monkeypatch.setattr(requests, "post", dummy_post)
    
    client = AmazonAdsClient()
    token = client.get_access_token()
    # On error, our method returns an empty string.
    assert token == ""
