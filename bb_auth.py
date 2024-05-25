from bottle import route, run, template, request
import requests
import json
import os
import configparser

# File names
config_json_file_name = 'app_secrets_template.json'
config_ini_file_name = 'app_secrets_template.ini'

# Read the JSON configuration file
with open(config_json_file_name, 'r') as config_json_file:
    config_json = json.load(config_json_file)

# Read the INI configuration file
config_ini = configparser.ConfigParser()
config_ini.read(config_ini_file_name)

@route('/')
def index():
    print_string = f'''
        Welcome to the Blackbaud SKY API Authorization Code Generator!
        <br><br>
        Please go to this URL: <a href="https://oauth2.sky.blackbaud.com/authorization?client_id={config_json['sky_app_information']['app_id']}&response_type=code&redirect_uri={config_json['other']['redirect_uri']}">https://oauth2.sky.blackbaud.com/authorization?client_id={config_json['sky_app_information']['app_id']}&response_type=code&redirect_uri={config_json['other']['redirect_uri']}</a>
    '''
    return print_string

@route('/callback')
def callback():
    auth_code = request.query.code
    get_access_refresh_tokens(auth_code)
    return template('Your code is {{auth_code}}', auth_code=auth_code)

def get_access_refresh_tokens(auth_code):
    token_uri = 'https://oauth2.sky.blackbaud.com/token'
    params = {
        'grant_type': 'authorization_code',
        'redirect_uri': config_json['other']['redirect_uri'],
        'code': auth_code,
        'client_id': config_json['sky_app_information']['app_id'],
        'client_secret': config_json['sky_app_information']['app_secret']
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_uri, data=params, headers=headers)
    response_data = response.json()
    print("Token response:", response_data)

    if 'access_token' in response_data and 'refresh_token' in response_data:
        access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']
        config_json['tokens']['access_token'] = access_token
        config_json['tokens']['refresh_token'] = refresh_token

        # Update JSON file
        with open(config_json_file_name, 'w') as config_json_file:
            json.dump(config_json, config_json_file, indent=4)
        print("Tokens updated in JSON file.")

        # Update INI file
        update_ini_file(access_token, refresh_token)
    else:
        print("Error: Tokens not found in the response.")

def update_ini_file(access_token, refresh_token):
    config_ini['tokens'] = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    with open(config_ini_file_name, 'w') as config_ini_file:
        config_ini.write(config_ini_file)
    print("Tokens updated in INI file.")

run(host='localhost', port=13631, debug=True)
