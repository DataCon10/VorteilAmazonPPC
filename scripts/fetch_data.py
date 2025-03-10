import logging
import requests
from dotenv import load_dotenv
from config import (
    CLIENT_ID, 
    CLIENT_SECRET, 
    REFRESH_TOKEN,  
    AMAZON_REDIRECT_URI,  
    TOKEN_URL,  
    CAMPAIGNS_ENDPOINT,
    PROFILES_ENDPOINT,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()


class AmazonAdsClient:
    def __init__(self):
        # CHANGED: Initialize instance variables from configuration.
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.refresh_token = REFRESH_TOKEN
        self.redirect_uri = AMAZON_REDIRECT_URI
        self.token_url = TOKEN_URL
        self.campaigns_endpoint = CAMPAIGNS_ENDPOINT
        self.profiles_endpoint = PROFILES_ENDPOINT
        self.token = None


    def get_access_token(self) -> str:
        """
        Exchange your refresh token for a new access token.
        Returns:
            access_token (str): A new access token.
        """
        payload = {
            "grant_type": "refresh_token",  # CHANGED: Using refresh token grant
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
            # Note: redirect_uri is typically not required for refresh token exchange.
        }
        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            logging.info("Access Token obtained successfully: %s", access_token)
            self.token = access_token
            return access_token
        else:
            logging.error("Error obtaining token: %s %s", response.status_code, response.text)
            return ""


    def build_headers(self, token: str, profile_id: str = None) -> dict:
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
            "Amazon-Advertising-API-ClientId": self.client_id
        }
        if profile_id:
            headers["Amazon-Advertising-API-Scope"] = profile_id
        return self.headers


    def get_profiles(self) -> list:
        """
        Fetch all advertising profiles using the provided access token.
        Returns:
            profiles (list): List of profile objects.
        """
        if not self.token:
            self.get_access_token()

        headers = self.build_headers(self.token)
        response = requests.get(self.profiles_endpoint, headers=headers)
        if response.status_code == 200:
            profiles = response.json()
            logging.info("Profiles fetched successfully: %s", profiles)
            return profiles
        else:
            logging.error("Error fetching profiles: %s %s", response.status_code, response.text)
            return []


    def get_uk_profile_id(self, profiles: list) -> str:
        """
        Filter the list of profiles for the UK.
        Args:
            profiles (list): List of profile objects.
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


    def fetch_campaigns(self, profile_id: str) -> dict:
        """
        Fetch the PPC campaign data using the access token and profile ID.
        Returns:
            campaigns (dict): JSON response with campaign data.
        """
        if not self.token:
            self.get_access_token()
        headers = self.build_headers(self.token, profile_id)
        response = requests.get(self.campaigns_endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Error fetching campaigns: %s %s", response.status_code, response.text)
            return {}


    def fetch_auto_campaign_search_terms(self, campaign_id: str) -> List[Dict]:
        """
        Fetches the search term report for a given auto campaign.
        Note: Replace this with the correct endpoint/method as per Amazon's Advertising API docs.
        
        Args:
            campaign_id (str): The ID of the auto campaign.
            
        Returns:
            List[Dict]: A list of search term performance dictionaries.
        """
        # Example endpoint for search term reports (this is illustrative)
        SEARCH_TERM_REPORT_ENDPOINT = f"https://advertising-api-eu.amazon.com/v2/campaigns/{campaign_id}/searchTermReport"
        
        headers = self.build_headers(self.token)  # assuming self.token is fresh
        response = requests.get(SEARCH_TERM_REPORT_ENDPOINT, headers=headers)
        if response.status_code == 200:
            return response.json()  # assuming this returns a list of dicts
        else:
            logging.error("Error fetching search term report: %s %s", response.status_code, response.text)
            return []



