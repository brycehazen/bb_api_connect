import json
import requests
from BbApiConnector import BbApiConnector
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_public_key():
    logger.debug("Starting get_public_key function")
    
    # Initialize the API connector
    connector = BbApiConnector()
    
    # Print the token response and subscription key
    try:
        token_response = connector._config['tokens']
        api_subscription_key = connector._config['other']['api_subscription_key']
        
        token_response_str = json.dumps(token_response, indent=4)
        print(f"Token response:\n{token_response_str}")
        print(f"API Subscription Key: {api_subscription_key}")
    except Exception as e:
        logger.error(f"Error obtaining token response or API subscription key: {e}")
        return
    
    # Get the authenticated session
    try:
        session = connector.get_session()
        logger.debug("Obtained authenticated session")
    except Exception as e:
        logger.error(f"Error obtaining authenticated session: {e}")
        return
    
    # Define the endpoint for retrieving the public key
    public_key_endpoint = 'https://api.sky.blackbaud.com/payments/v1/checkout/publickey'
    
    # Make the API request
    try:
        logger.debug(f"Making GET request to {public_key_endpoint}")
        response = session.get(public_key_endpoint)
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
            public_key_data = response.json()
            public_key = public_key_data.get('public_key')
            logger.debug(f"Public key data: {public_key_data}")
            
            # Print the retrieved public key
            if public_key:
                print(f"Public Key: {public_key}")
                logger.info(f"Public Key: {public_key}")
            
            # Optionally, save the public key to a file
            with open('public_key.json', 'w') as file:
                json.dump(public_key_data, file, indent=4)
            logger.info("Public key saved to public_key.json")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing response: {e}")
    else:
        logger.error(f"Failed to retrieve public key: {response.status_code} - {response.text}")

if __name__ == '__main__':
    get_public_key()
