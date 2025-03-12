"""
This script demonstrates how to exchange an authorization code for
an access token and a refresh token using Amazon's OAuth 2.0 flow.

IMPORTANT:
    Prerequisites:
        1. Register your application in the Amazon Developer Console.
        2. Set the redirect URI in your LWA app settings (e.g., https://amazon.com).
        3. Generate an authorization code by visiting:
            https://www.amazon.com/ap/oa?client_id=YOUR_CLIENT_ID&scope=cpc_advertising:campaign_management%20offline_access&response_type=code&redirect_uri=http://localhost:5000/callback
        4. Copy the 'code' parameter from the redirect URI.
        5. Place your credentials and the auth code in a .env file.

Usage:
    - Update the .env file with your AMAZON_CLIENT_ID, AMAZON_CLIENT_SECRET, AUTH_CODE, and AMAZON_REDIRECT_URI.
    - Run this script to retrieve your access and refresh tokens.
"""

import logging
import os
import requests
from dotenv import load_dotenv
from typing import Tuple

logging.basicConfig(level=logging.INFO)

# Load environment variables from your .env file
load_dotenv()

CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTH_CODE")            # The authorization code from user consent
REDIRECT_URI = os.getenv("AMAZON_REDIRECT_URI")  # Must match the one registered with Amazon

TOKEN_URL = "https://api.amazon.co.uk/auth/o2/token"

def get_tokens() -> Tuple[str, str]:
    """
    Exchange the authorization code for an access token and a refresh token.

    Returns:
        A tuple (access_token, refresh_token) if successful; otherwise, (None, None).
    """
    payload = {
        "grant_type": "authorization_code",  # Exchanging an auth code
        "code": AUTH_CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    logging.info("Requesting tokens with payload: %s", payload)
    response = requests.post(TOKEN_URL, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        logging.info("Access Token obtained successfully: %s", access_token)
        logging.info("Refresh Token obtained successfully: %s", refresh_token)
        return access_token, refresh_token
    else:
        logging.error("Error obtaining tokens: %s %s", response.status_code, response.text)
        return None, None

if __name__ == "__main__":
    get_tokens()
