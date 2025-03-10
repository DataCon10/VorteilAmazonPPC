from scripts import fetch_data, peel
import logging

logging.basicConfig(level=logging.INFO)

def main():

    # Create an instance of the client.
    client = fetch_data.AmazonAdsClient()
    
    # Retrieve an access token.
    token = client.get_access_token()
    if token:
        # Fetch profiles and get the UK profile ID.
        profiles = client.get_profiles()
        uk_profile_id = client.get_uk_profile_id(profiles)
        if uk_profile_id:
            logging.info("UK Profile ID: %s", uk_profile_id)
            # Fetch campaign data using the UK profile ID.
            campaigns = client.fetch_campaigns(uk_profile_id)
            if campaigns:
                logging.info("Campaign Data: %s", campaigns)
        else:
            logging.error("Could not locate a UK profile.")
    else:
        logging.error("No access token obtained.")

if __name__ == "__main__":
   main()