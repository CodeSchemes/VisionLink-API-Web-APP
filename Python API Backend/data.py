'''
This program pulls data from Vision Links CAT API and inserts it into a docker dashboard for ease of data visualization
Author: William Brown
Date: 9/15/2025
'''
import pandas as pd
import json
from json import loads, dumps
import http.client, urllib.request, urllib.parse, urllib.error, base64
import uuid
import requests
from dotenv import load_dotenv
import os

#.env file must be locally placed in the same folder as the web app 
load_dotenv()
token_url = os.getenv('token_url')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
scope = os.getenv('scope')

# Function to get a new access token
def generate_access_token():
    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")
    data = { #data perameters for token generation authoirization ('client_id', 'client_secret', 'scope', 'grant_type')
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=data, headers=headers)
    return f"Bearer {response.json().get('access_token')}"

access_token = generate_access_token()

def generate_tracking_id():
    """
    Generates a version 4 UUID and returns it as a string,
    compatible with java.util.UUID.
    """
    # Generate a random UUID object
    uuid_obj = uuid.uuid4()
    
    # Convert the UUID object to its canonical string representation
    tracking_id = str(uuid_obj)
    
    return tracking_id



def pull_asset_summaries(headers=None):
    #conn: set locally within the function and globally inside the module that contains this function
    conn = http.client.HTTPSConnection('services.cat.com')
    
    #Calls generate_access_token and generate_tracking_id functions to be assigned to their respective variables for use in the headers dictionary
    access_token = generate_access_token()
    x_cat_api_tracking_id = generate_tracking_id()

    #headers is used to store the authorization token and tracking id for use in the API request
    headers = {
    'Authorization': access_token,
    'X-Cat-API-Tracking-Id': f'{x_cat_api_tracking_id}',
    }
    #Parameters to filter data being pulled in
    params = urllib.parse.urlencode({
        
    })
    conn.request("GET", "/catDigital/assetSummary/v1/assets?%s" % params, headers = headers)
    response = conn.getresponse()
    data = response.read()
    input = json.loads(data)
    df = pd.json_normalize(input['assetSummaries'], errors='ignore')
    df = df.to_json(orient='split')
    df = loads(df)
    conn.close()
    #print(f"Pulled {len(df)} records from Asset Summaries")
    return dumps(df, indent = 4)

def pull_fault_codes(params='', headers=None):
    conn = http.client.HTTPSConnection('services.cat.com')
    access_token = generate_access_token()
    x_cat_api_tracking_id = generate_tracking_id()
    headers = {
    'Authorization': access_token,
    'X-Cat-API-Tracking-Id': f'{x_cat_api_tracking_id}',
    }
    conn.request("GET", "/catDigital/faultsHistory/v1/faults?%s" % params, headers = headers)
    response = conn.getresponse()
    data = response.read()
    input = json.loads(data)
    df = pd.json_normalize(input['faults'], errors='ignore')
    df = df.to_json(orient='split')
    df = loads(df)
    conn.close()
    #print(f"Pulled {len(df)} records from Asset Summaries")
    return dumps(df, indent = 4)
    
conn = http.client.HTTPSConnection('services.cat.com')
try:
    conn.close()
except Exception as e:
    print(e)





