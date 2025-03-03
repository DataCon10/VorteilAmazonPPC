import os
import requests
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

# Retrieve your credentials and authorization details from the .env file
CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTH_CODE")        # The authorization code from user consent
REDIRECT_URI = "https://amazon.com"    # Must match the one registered with Amazon

# Amazon OAuth token endpoint (verify with the latest documentation)
TOKEN_URL = "https://api.amazon.co.uk/auth/o2/token"
# Amazon Advertising API endpoint for campaigns (adjust region/version as needed)
CAMPAIGNS_ENDPOINT = "https://advertising-api.amazon.com/v2/campaigns"

PROFILES_ENDPOINT = "https://advertising-api-eu.amazon.com/v2/profiles"

def get_access_token():
    """Exchange the authorization code for an access token."""
    payload = {
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        print("Access Token obtained successfully.")
        return access_token
    else:
        print("Error obtaining token:", response.status_code, response.text)
        return None


def get_profiles(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Amazon-Advertising-API-ClientId": CLIENT_ID,
        "Content-Type": "application/json"
    }

    response = requests.get(PROFILES_ENDPOINT, headers=headers)
    if response.status_code == 200:
        profiles = response.json()
        print("Profiles fetched successfully:")
        print(profiles)
        return profiles
    else:
        print("Error fetching profiles:", response.status_code, response.text)
        return None


def fetch_campaigns(access_token):
    """Fetch the PPC campaign data using the access token."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(CAMPAIGNS_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching campaigns:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    token = get_access_token()
    if token:
        profiles = get_profiles(token)
        campaigns = fetch_campaigns(token)
        if campaigns:
            print("Campaign Data:")
            print(campaigns)
