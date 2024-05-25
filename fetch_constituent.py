import json
import requests
from BbApiConnector import BbApiConnector
from datetime import datetime

def get_constituent(session, constituent_id):
    url = f"https://api.sky.blackbaud.com/constituent/v1/constituents/{constituent_id}"
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("401 Unauthorized. Refreshing access token...")
        connector.update_access_token()
        session.headers.update({'Authorization': f"Bearer {connector._config['tokens']['access_token']}"})
        response = session.get(url)
        if response.status_code == 200:
            return response.json()
    print(f"Error: {response.status_code} - {response.text}")
    return None

connector = BbApiConnector()

def safe_get(dictionary, keys, default=""):
    """
    Safely get a nested value from a dictionary.
    :param dictionary: The dictionary to get the value from.
    :param keys: A list of keys representing the nested path.
    :param default: The default value to return if any key is not found.
    :return: The value if found, otherwise the default value.
    """
    for key in keys:
        dictionary = dictionary.get(key)
        if dictionary is None:
            return default
    return dictionary

# Prompt user for the constituent ID
constituent_id = input("Please enter the System record ID of the constituent: ")
connector = BbApiConnector()
session = connector.get_session()
constituent_data = get_constituent(session, constituent_id)
# Assuming 'constituent_data' contains the date strings
date_added = datetime.fromisoformat(constituent_data.get('date_added')).strftime('%B %d, %Y %H:%M:%S')
date_modified = datetime.fromisoformat(constituent_data.get('date_modified')).strftime('%B %d, %Y %H:%M:%S')

if constituent_data:
    print(f"Request URL: https://api.sky.blackbaud.com/constituent/v1/constituents/{constituent_id}")
    print("Response status code: 200\n")
    print("Constituent Details:\n")
    print(f"    ID: {safe_get(constituent_data, ['id'])}")
    print(f"    Name: {safe_get(constituent_data, ['name'])}")
    print(f"    First Name: {safe_get(constituent_data, ['first'])}")
    print(f"    Last Name: {safe_get(constituent_data, ['last'])}")
    print(f"    Title: {safe_get(constituent_data, ['title'])}")
    print(f"    Gender: {safe_get(constituent_data, ['gender'])}")
    print(f"    Age: {safe_get(constituent_data, ['age'])}")

    birthdate = safe_get(constituent_data, ['birthdate'], {})
    formatted_birthdate = f"{birthdate.get('d', '')}/{birthdate.get('m', '')}/{birthdate.get('y', '')}"
    print(f"    Birthdate: {formatted_birthdate}")

    print(f"    Marital Status: {safe_get(constituent_data, ['marital_status'])}")
    print(f"    Fundraiser Status: {safe_get(constituent_data, ['fundraiser_status'])}")
    print(f"    Gives Anonymously: {safe_get(constituent_data, ['gives_anonymously'])}")
    print(f"    Deceased: {safe_get(constituent_data, ['deceased'])}")
    print(f"    Inactive: {safe_get(constituent_data, ['inactive'])}")
    print(f"    Type: {safe_get(constituent_data, ['type'])}")
    print(f"    Is Memorial: {safe_get(constituent_data, ['is_memorial'])}")
    print(f"    Is Solicitor: {safe_get(constituent_data, ['is_solicitor'])}")
    print(f"    No Valid Address: {safe_get(constituent_data, ['no_valid_address'])}")
    print(f"    Receipt Type: {safe_get(constituent_data, ['receipt_type'])}")
    print(f"    Requests No Email: {safe_get(constituent_data, ['requests_no_email'])}")
    print(f"    Import ID: {safe_get(constituent_data, ['import_id'])}")
    print(f"    Is Constituent: {safe_get(constituent_data, ['is_constituent'])}")
    print(f"    Lookup ID: {safe_get(constituent_data, ['lookup_id'])}\n")

    print("Address:\n")
    address = safe_get(constituent_data, ['address'], {})
    print(f"    ID: {safe_get(address, ['id'])}")
    print(f"    Address Lines: {safe_get(address, ['address_lines'])}")
    print(f"    City: {safe_get(address, ['city'])}")
    print(f"    State: {safe_get(address, ['state'])}")
    print(f"    Postal Code: {safe_get(address, ['postal_code'])}")
    print(f"    Country: {safe_get(address, ['country'])}")
    print(f"    County: {safe_get(address, ['county'])}")
    print(f"    Preferred: {safe_get(address, ['preferred'])}")
    print(f"    Start Date: {safe_get(address, ['start_date'])}")
    print(f"    Formatted Address: {safe_get(address, ['formatted_address'])}")
    print(f"    Do Not Mail: {safe_get(address, ['do_not_mail'])}")
    print(f"    Inactive: {safe_get(address, ['inactive'])}")
    print(f"    Type: {safe_get(address, ['type'])}\n")

    print("Email:\n")
    email = safe_get(constituent_data, ['email'], {})
    print(f"    ID: {safe_get(email, ['id'])}")
    print(f"    Address: {safe_get(email, ['address'])}")
    print(f"    Primary: {safe_get(email, ['primary'])}")
    print(f"    Do Not Email: {safe_get(email, ['do_not_email'])}")
    print(f"    Inactive: {safe_get(email, ['inactive'])}")
    print(f"    Type: {safe_get(email, ['type'])}\n")

    print("Phone:\n")
    phone = safe_get(constituent_data, ['phone'], {})
    print(f"    ID: {safe_get(phone, ['id'])}")
    print(f"    Number: {safe_get(phone, ['number'])}")
    print(f"    Primary: {safe_get(phone, ['primary'])}")
    print(f"    Do Not Call: {safe_get(phone, ['do_not_call'])}")
    print(f"    Inactive: {safe_get(phone, ['inactive'])}")
    print(f"    Type: {safe_get(phone, ['type'])}\n")

    print("Spouse:\n")
    spouse = safe_get(constituent_data, ['spouse'], {})
    print(f"    ID: {safe_get(spouse, ['id'])}")
    print(f"    First Name: {safe_get(spouse, ['first_name'])}")
    print(f"    Last Name: {safe_get(spouse, ['last_name'])}")
    print(f"    Is Head of Household: {safe_get(spouse, ['is_head_of_household'])}\n")

    date_added = safe_get(constituent_data, ['date_added'])
    date_modified = safe_get(constituent_data, ['date_modified'])

    if date_added != "":
        date_added = datetime.fromisoformat(date_added).strftime('%B %d, %Y %H:%M:%S')
    if date_modified != "":
        date_modified = datetime.fromisoformat(date_modified).strftime('%B %d, %Y %H:%M:%S')

    print("Date Information:\n")
    print(f"    Date Added: {date_added}")
    print(f"    Date Modified: {date_modified}")
else:
    print("Failed to retrieve constituent data.")