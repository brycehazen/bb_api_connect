import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BbApiConnector(object):
    def __init__(self, config_file_name=None):
        if config_file_name is None:
            config_file_name = os.path.join(os.path.dirname(__file__), 'app_secrets_template.json')
        self.config_file_name = config_file_name
        with open(self.config_file_name, 'r') as file:
            self._config = json.load(file)
        logger.debug('Configuration loaded from %s', self.config_file_name)

    def get_session(self):
        session = requests.Session()
        session.headers = {
            'Bb-Api-Subscription-Key': self._config['other']['api_subscription_key'],
            'Authorization': f"Bearer {self._config['tokens']['access_token']}"
        }
        return session

    # Comment out or remove the update_access_token method to prevent updating tokens
    # def update_access_token(self):
    #     token_uri = 'https://oauth2.sky.blackbaud.com/token'
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #     params = {
    #         'grant_type': 'refresh_token',
    #         'refresh_token': self._config['tokens']['refresh_token'],
    #         'preserve_refresh_token': True,
    #         'client_id': self._config['sky_app_information']['app_id'],
    #         'client_secret': self._config['sky_app_information']['app_secret']
    #     }
    #     try:
    #         response = requests.post(token_uri, data=params, headers=headers)
    #         response.raise_for_status()  # Raise an error for bad status codes
    #         response_data = response.json()
    #         logger.debug('Token refresh response: %s', response_data)

    #         if 'access_token' in response_data:
    #             self._config['tokens']['access_token'] = response_data['access_token']
    #             with open(self.config_file_name, 'w') as config_file:
    #                 json.dump(self._config, config_file, indent=4)
    #             logger.info("Access token updated.")
    #         else:
    #             logger.error("access_token not found in the response: %s", response_data)
    #             raise KeyError("access_token not found in the response")
    #     except requests.exceptions.RequestException as e:
    #         logger.error("Request failed: %s", e)
    #         raise

if __name__ == '__main__':
    connector = BbApiConnector()
    # The following lines are commented out to prevent updating the access token
    # try:
    #     connector.update_access_token()
    # except Exception as e:
    #     logger.error("Failed to update access token: %s", e)
