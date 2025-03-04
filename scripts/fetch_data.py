import requests
from dotenv import load_dotenv

from config import (
    CLIENT_ID, 
    CLIENT_SECRET, 
    REFRESH_TOKEN,  # CHANGED: Using refresh token instead of auth code
    AMAZON_REDIRECT_URI,  # Using variable from config
    TOKEN_URL,  # Already set from config
    CAMPAIGNS_ENDPOINT,
    PROFILES_ENDPOINT,
)


# Load environment variables from your .env file
load_dotenv()

def get_access_token():
    """
    Exchange your refresh token for a new access token.
    CHANGED: Using 'refresh_token' grant instead of 'authorization_code'
    """
    payload = {
        "grant_type": "refresh_token", 
        "refresh_token": REFRESH_TOKEN, 
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        print("Access Token obtained successfully:")
        print(access_token)
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

def get_uk_profile_id(profiles):
    """
    CHANGED: Filter profiles for the UK.
    Assuming that the UK profile has a 'countryCode' field set to 'GB'.
    Adjust the filter if your profiles use a different identifier.
    """
    for profile in profiles:
        # Check if the profile has a countryCode field and if it's 'GB' (United Kingdom)
        if profile.get("countryCode") == "UK":
            return str(profile.get("profileId"))
    print("UK profile not found.")
    return None


def fetch_campaigns(access_token, profile_id):
    """Fetch the PPC campaign data using the access token and profile ID."""
    # CHANGED: Added Amazon-Advertising-API-Scope header with the profile_id.
    headers = {
        "Amazon-Advertising-API-ClientId": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Amazon-Advertising-API-Scope": profile_id  # Required header for campaigns endpoint
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
        uk_profile_id = get_uk_profile_id(profiles)
        campaigns = fetch_campaigns(token, uk_profile_id)
        if campaigns:
            print("Campaign Data:")
            print(campaigns)
