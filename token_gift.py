import json
import requests
from BbApiConnector import BbApiConnector

def get_recurring_gift_tokens():
    # Initialize the API connector
    connector = BbApiConnector()
    
    # Update access token if needed
    try:
        connector.update_access_token()
    except KeyError as e:
        print(f"Error updating access token: {e}")
        return
    
    # Get the authenticated session
    session = connector.get_session()
    
    # Define the endpoint for retrieving recurring gifts
    recurring_gifts_endpoint = 'https://api.sky.blackbaud.com/gift/v1/recurring_gifts'
    
    # Make the API request
    response = session.get(recurring_gifts_endpoint)
    
    if response.status_code == 200:
        recurring_gifts = response.json()
        tokens = []
        
        for gift in recurring_gifts.get('value', []):
            token = gift.get('token')
            if token:
                tokens.append({
                    'gift_id': gift.get('id'),
                    'token': token
                })
        
        # Print the retrieved tokens
        for item in tokens:
            print(f"Gift ID: {item['gift_id']}, Token: {item['token']}")
        
        # Optionally, save the tokens to a file
        with open('recurring_gift_tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)
        print("Tokens saved to recurring_gift_tokens.json")
    
    else:
        print(f"Failed to retrieve recurring gifts: {response.status_code} - {response.text}")

if __name__ == '__main__':
    get_recurring_gift_tokens()
