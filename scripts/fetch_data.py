import logging
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

logging.basicConfig(level=logging.INFO)


# Load environment variables from your .env file
load_dotenv()

def get_access_token() -> str:
    """
    Exchange your refresh token for a new access token.
    Returns:
        access_token (str): A new access token.
    """
    payload = {
        "grant_type": "refresh_token",  # CHANGED: Use refresh token grant
        "refresh_token": REFRESH_TOKEN,   # CHANGED: Use the refresh token from .env
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        logging.info("Access Token obtained successfully: %s", access_token)
        return access_token
    else:
        logging.error("Error obtaining token: %s %s", response.status_code, response.text)
        return ""


def get_profiles(token: str) -> list:
    """
    Fetch all advertising profiles using the provided access token.
    Returns:
        profiles (list): List of profile objects.
    """
    headers = build_headers(token)
    response = requests.get(PROFILES_ENDPOINT, headers=headers)
    if response.status_code == 200:
        profiles = response.json()
        logging.info("Profiles fetched successfully: %s", profiles)
        return profiles
    else:
        logging.error("Error fetching profiles: %s %s", response.status_code, response.text)
        return []

def get_uk_profile_id(profiles: list) -> str:
    """
    Filter the list of profiles for the UK.
    Returns:
        The profileId as a string if found, or an empty string.
    Note: Typically the country code is 'GB'. Adjust if necessary.
    """
    for profile in profiles:
        # CHANGED: Check if the profile has countryCode 'UK' (or 'GB' if appropriate)
        if profile.get("countryCode") in ("UK", "GB"):
            return str(profile.get("profileId"))
    logging.error("UK profile not found.")
    return ""


def fetch_campaigns(access_token: str, profile_id: str) -> dict:
    """
    Fetch the PPC campaign data using the access token and profile ID.
    Returns:
        campaigns (dict): JSON response with campaign data.
    """
    headers = build_headers(access_token, profile_id)
    response = requests.get(CAMPAIGNS_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error fetching campaigns: %s %s", response.status_code, response.text)
        return {}

def build_headers(token: str, profile_id: str = None) -> dict:
    """
    Build common headers for Amazon Advertising API requests.
    Args:
        token (str): The access token.
        profile_id (str, optional): The profile ID, if needed.
    Returns:
        headers (dict): Dictionary of headers.
    """
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json",
        "Amazon-Advertising-API-ClientId": CLIENT_ID
    }
    if profile_id:
        headers["Amazon-Advertising-API-Scope"] = profile_id
    return headers


if __name__ == "__main__":
    token = get_access_token()
    if token:
        profiles = get_profiles(token)
        uk_profile_id = get_uk_profile_id(profiles)
        if uk_profile_id:
            logging.info("UK Profile ID: %s", uk_profile_id)
            campaigns = fetch_campaigns(token, uk_profile_id)
            if campaigns:
                logging.info("Campaign Data: %s", campaigns)
        else:
            logging.error("Could not locate a UK profile.")
    else:
        logging.error("No access token obtained.")