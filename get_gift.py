import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BbApiConnector:
    def __init__(self, config_file_name=None):
        if config_file_name is None:
            config_file_name = 'app_secrets_template.json'
        with open(config_file_name, 'r') as file:
            self._config = json.load(file)
        logger.debug(f'Configuration loaded from {config_file_name}')
    
    def get_session(self):
        session = requests.Session()
        session.headers = {
            'Bb-Api-Subscription-Key': self._config['other']['api_subscription_key'],
            'Authorization': f"Bearer {self._config['tokens']['access_token']}"
        }
        return session

def get_gift_info(gift_id):
    logger.debug("Starting get_gift_info function")
    
    # Initialize the API connector
    connector = BbApiConnector()
    
    # Print subscription key and refresh token
    try:
        api_subscription_key = connector._config['other']['api_subscription_key']
        refresh_token = connector._config['tokens']['refresh_token']
        
        print(f"API Subscription Key: {api_subscription_key}")
        print(f"Refresh Token: {refresh_token}")
        
    except Exception as e:
        logger.error(f"Error obtaining API subscription key or refresh token: {e}")
        return
    
    # Get the authenticated session
    try:
        session = connector.get_session()
        logger.debug("Obtained authenticated session")
    except Exception as e:
        logger.error(f"Error obtaining authenticated session: {e}")
        return
    
    # Define the endpoint for retrieving the gift information
    gift_endpoint = f'https://api.sky.blackbaud.com/gift/v1/gifts/{gift_id}'
    
    # Make the API request
    try:
        logger.debug(f"Making GET request to {gift_endpoint}")
        response = session.get(gift_endpoint)
        logger.debug(f"Response status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"RequestException during GET request: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during GET request: {e}")
        return
    
    if response.status_code == 200:
        logger.debug("Request successful")
        try:
            gift_data = response.json()
            logger.debug(f"Gift data: {gift_data}")
            
            # Print the retrieved gift data
            print("Gift Information:")
            print(json.dumps(gift_data, indent=4))
            
            # Print payment details if they exist
            if 'payments' in gift_data and gift_data['payments']:
                print("\nPayments:")
                for payment in gift_data['payments']:
                    print(json.dumps(payment, indent=4))
            
            # Optionally, save the gift data to a file
            with open('gift_data.json', 'w') as file:
                json.dump(gift_data, file, indent=4)
            logger.info("Gift data saved to gift_data.json")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing response: {e}")
    else:
        logger.error(f"Failed to retrieve gift information: {response.status_code} - {response.text}")

if __name__ == '__main__':
    gift_id = input("Enter the gift ID: ")
    get_gift_info(gift_id)
