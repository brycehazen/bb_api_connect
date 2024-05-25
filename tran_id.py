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

def get_transaction_info(transaction_id):
    logger.debug("Starting get_transaction_info function")
    
    # Initialize the API connector
    connector = BbApiConnector()
    
    # Get the authenticated session
    try:
        session = connector.get_session()
        logger.debug("Obtained authenticated session")
    except Exception as e:
        logger.error(f"Error obtaining authenticated session: {e}")
        return
    
    # Define the endpoint for retrieving the transaction information
    transaction_endpoint = f'https://api.sky.blackbaud.com/payments/v1/transactions/{transaction_id}'
    
    # Make the API request
    try:
        logger.debug(f"Making GET request to {transaction_endpoint}")
        response = session.get(transaction_endpoint)
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
            transaction_data = response.json()
            logger.debug(f"Transaction data: {transaction_data}")
            
            # Print the retrieved transaction data
            print(json.dumps(transaction_data, indent=4))
            
            # Optionally, save the transaction data to a file
            with open('transaction_data.json', 'w') as file:
                json.dump(transaction_data, file, indent=4)
            logger.info("Transaction data saved to transaction_data.json")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing response: {e}")
    else:
        logger.error(f"Failed to retrieve transaction information: {response.status_code} - {response.text}")

if __name__ == '__main__':
    transaction_id = input("Enter the transaction ID: ")
    get_transaction_info(transaction_id)
