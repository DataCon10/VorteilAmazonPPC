# config.py
import os
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

# Set the target marketplace via an environment variable (default is EU)
MARKETPLACE = os.getenv("MARKETPLACE", "UK")  # Options: "US", "EU", "UK"

# Define endpoints for each marketplace
ENDPOINTS = {
    "US": {
        "TOKEN_URL": "https://api.amazon.com/auth/o2/token",
        "CAMPAIGNS_ENDPOINT": "https://advertising-api.amazon.com/v2/campaigns",
        "PROFILES_ENDPOINT": "https://advertising-api.amazon.com/v2/profiles",
    },
    "EU": {
        "TOKEN_URL": "https://api.amazon.com/auth/o2/token",  # Global token endpoint works for EU
        "CAMPAIGNS_ENDPOINT": "https://advertising-api-eu.amazon.com/v2/campaigns",
        "PROFILES_ENDPOINT": "https://advertising-api-eu.amazon.com/v2/profiles",
    },
    "UK": {
        "TOKEN_URL": "https://api.amazon.co.uk/auth/o2/token",
        "CAMPAIGNS_ENDPOINT": "https://advertising-api-eu.amazon.com/v2/campaigns",
        "PROFILES_ENDPOINT": "https://advertising-api-eu.amazon.com/v2/profiles",
    },
}

# Select the endpoints for the chosen marketplace
TOKEN_URL = ENDPOINTS[MARKETPLACE]["TOKEN_URL"]
CAMPAIGNS_ENDPOINT = ENDPOINTS[MARKETPLACE]["CAMPAIGNS_ENDPOINT"]
PROFILES_ENDPOINT = ENDPOINTS[MARKETPLACE]["PROFILES_ENDPOINT"]

# Load your Amazon Advertising API credentials from environment variables
CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTH_CODE")  # Only used in the initial OAuth flow
AMAZON_REDIRECT_URI = os.getenv("AMAZON_REDIRECT_URI")  # Must match your registered URI
REFRESH_TOKEN = os.getenv("AMAZON_REFRESH_TOKEN")  # CHANGED: New variable for refresh token

