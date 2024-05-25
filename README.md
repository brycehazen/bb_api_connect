
# Blackbaud API Connector

This project provides a simple connector to the Blackbaud SKY API, including authentication and API request handling. The provided scripts include methods for obtaining access and refresh tokens, and making authenticated requests to the Blackbaud API.

## Files

- `bb_api_connect.py`: Handles API requests using the Blackbaud SKY API.
- `bb_auth.py`: Facilitates the OAuth2 authentication flow to obtain access and refresh tokens.
- `app_secrets_template.json`: Template for storing application secrets and tokens.
- `app_secrets_template.ini`: Alternative configuration file for storing tokens (updated after authentication).
- Any other .py that has your endpoint, put in the same directory as the files above. 

## Setup

### Prerequisites

- Python 3.x
- `requests` library
- `bottle` web framework
- In developer.blackbaud.com/apps, under Redirect URIs, that you have http://localhost:13631/callback as an option.
- app.blackbaud.com/marketplace, under the Manage tab - link your application to an environment.
- app.blackbaud.com/marketplace - linked application scopes are approved. Scopes are set from developer.blackbaud.com/apps

Install the required libraries using pip:

```sh
pip install requests bottle
```

### Configuration

1. **Update the `app_secrets_template.json` file**:
   
   - Fill in the `app_id` and `app_secret` fields with the values obtained from creating an application in Blackbaud.
   - Set the `redirect_uri` to `http://localhost:13631/callback`.
   - Update the `api_subscription_key` with the key found under your Developer account.

   Example:

   ```json
   {
       "sky_app_information": {
           "app_id": "Application ID (OAuth client_id) after creating an application",
           "app_secret": "Primary application secret after creating an application"
       },
       "tokens": {
           "access_token": "From http://localhost:13631/ after running bb_auth.py and login to blackbaud, will print to console - VERY LONG",
           "refresh_token": response from localhost:13631 - Much shorter"
       },
       "other": {
           "api_subscription_key": "Primary access key found under Developer account",
           "redirect_uri": "http://localhost:13631/callback",
           "test_api_endpoint": "I put the endpoints in the .py file using bb_api_connect"
       }
   }

   ```

2. **Update the `app_secrets_template.ini` file (optional)**:

   This file will be automatically updated after successful authentication with access and refresh tokens.

### Running the Authentication Server

To obtain access and refresh tokens, run the authentication server:

```sh
python bb_auth.py
```

1. Open your browser and navigate to the URL provided by the server.
2. Authorize the application and capture the authorization code.
3. The server will handle the token exchange and update the `app_secrets_template.json` and `app_secrets_template.ini` files with the obtained tokens.

### Making API Requests

The `bb_api_connect.py` script is used to make authenticated requests to the Blackbaud API. 

Example usage:

```python
from bb_api_connect import bb_api_connect

connector = bb_api_connect()
session = connector.get_session()

# Example API request
response = session.get("https://api.sky.blackbaud.com/constituent/v1/constituents")
print(response.json())
```

### Notes

- The `bb_api_connect` class currently has the `update_access_token` method commented out to prevent automatic token updates. Uncomment and use it if you need to refresh tokens programmatically.
- The `bb_auth.py` script handles the initial OAuth2 flow and should be run whenever you need to refresh or obtain new tokens.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
