import pytest
import importlib

from vorteilamazonppc.scripts.fetch_data import AmazonAdsClient

def test_amazon_ads_client_setup():
    importlib.reload()
    client = AmazonAdsClient()
    assert client.client_id == "test_client_id"
    assert client.client_secret == "test_client_secret"
    assert client.refresh_token == "test_refresh_token"
    assert client.redirect_uri == "http://localhost:5000/callback"
