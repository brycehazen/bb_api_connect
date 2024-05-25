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

def get_payment_configurations(include_inactive=False):
    logger.debug("Starting get_payment_configurations function")
    
    # Initialize the API connector
    connector = BbApiConnector()
    
    # Get the authenticated session
    try:
        session = connector.get_session()
        logger.debug("Obtained authenticated session")
    except Exception as e:
        logger.error(f"Error obtaining authenticated session: {e}")
        return
    
    # Define the endpoint for retrieving the payment configurations
    public_key_endpoint = 'https://api.sky.blackbaud.com/payments/v1/paymentconfigurations'
    params = {'include_inactive': str(include_inactive).lower()}
    
    # Make the API request
    try:
        logger.debug(f"Making GET request to {public_key_endpoint} with params {params}")
        response = session.get(public_key_endpoint, params=params)
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
            payment_configurations = response.json()
            logger.debug(f"Payment configurations data: {payment_configurations}")
            
            # Filter and print active payment configurations
            active_configs = [config for config in payment_configurations.get('value', []) if config.get('active')]
            for i, config in enumerate(active_configs, 1):
                print(f"{i}. {config['name']}")
            
            # Allow user to select a configuration to see full details
            try:
                selection = int(input("Enter the number of the configuration to see full details: ")) - 1
                if 0 <= selection < len(active_configs):
                    selected_config = active_configs[selection]
                    print(json.dumps(selected_config, indent=4))
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            
            # Optionally, save the payment configurations to a file
            with open('payment_configurations.json', 'w') as file:
                json.dump(payment_configurations, file, indent=4)
            logger.info("Payment configurations saved to payment_configurations.json")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing response: {e}")
    else:
        logger.error(f"Failed to retrieve payment configurations: {response.status_code} - {response.text}")

if __name__ == '__main__':
    # Call the function with include_inactive parameter
    get_payment_configurations(include_inactive=True)
