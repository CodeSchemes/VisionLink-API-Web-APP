'''
This program pulls data from Vision Links CAT API and inserts it into a docker dashboard for ease of data visualization
Author: William Brown
Date: 9/15/2025
'''
from time import perf_counter
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
    """
    Generates a Bearer token for CAT API authentication using client credentials flow.
    
    Parameters:
        None (uses module-level variables: client_id, client_secret, scope, token_url from .env)
    
    Returns:
        str: Bearer token in format "Bearer {access_token}"
    
    Limitations:
        - Requires .env file with token_url, client_id, client_secret, and scope variables
        - Depends on requests library for HTTP POST
        - Token expiry is not handled; caller should implement refresh logic if needed
        - Raises exception if token_url is unreachable or credentials are invalid
    """
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
    compatible with java.util.UUID for use in CAT API X-Cat-API-Tracking-Id header.
    
    Parameters:
        None
    
    Returns:
        str: UUID4 string in canonical format (e.g., "550e8400-e29b-41d4-a716-446655440000")
    
    Limitations:
        - Relies on uuid.uuid4() which requires os.urandom; may be slow on some systems
        - No validation that the UUID is actually used in a request
        - Each call generates a new ID; if you need to track a multi-step request, store and reuse
    """
    # Generate a random UUID object
    uuid_obj = uuid.uuid4()
    
    # Convert the UUID object to its canonical string representation
    tracking_id = str(uuid_obj)
    
    return tracking_id



def pull_asset_summaries(headers=None):
    """
    Pulls asset summary data from CAT Digital API and returns formatted JSON.
    
    Parameters:
        headers (dict, optional): Custom headers dict. If None, headers are auto-generated 
                                  with Authorization and X-Cat-API-Tracking-Id. Default: None
    
    Returns:
        str: JSON string (indent=4) containing asset data in split orient 
             (index, columns, data keys)
    
    Methods used:
        - http.client.HTTPSConnection: Opens HTTPS connection to services.cat.com
          Params: hostname (str), timeout (optional int)
          Returns: connection object with .request(), .getresponse(), .close()
          Limits: blocking I/O, manual connection management, no built-in retry
        
        - conn.request(method, url, body, headers): Sends HTTP request
          Params: method (str: GET/POST), url (str), body (optional), headers (dict)
          Limits: no automatic redirects, raw string formatting only
        
        - pd.json_normalize(): Flattens nested JSON into flat DataFrame
          Params: data (dict/list), errors (str: 'ignore'/'raise')
          Limits: can create many columns for deeply nested objects; all rows must match structure
        
        - df.to_json(orient): Converts DataFrame to JSON string
          Params: orient (str: 'split'/'records'/'index'/'columns')
          Limits: 'split' format less intuitive for frontend; large DataFrames may be slow
        
        - json.loads() / json.dumps(): Parse/serialize JSON strings
          Params: loads(str), dumps(obj, indent=int)
          Limits: does not handle circular references; indent increases output size
    
    Limitations:
        - Hardcoded connection to services.cat.com; no fallback or configuration
        - No error handling for network failures, malformed responses, or API rate limits
        - Access token and tracking ID regenerated each call (inefficient)
        - Empty params dict; filtering not implemented
        - Connection closed but no explicit error handling if close() fails
        - Assumes 'assetSummaries' key exists in response; KeyError if missing
        - No pagination; may fail on large datasets
    """
    start = perf_counter()
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
    raw_data = response.read()

    parsed = json.loads(raw_data)

    # Normalize into DataFrame
    df = pd.json_normalize(parsed.get("assetSummaries", []), errors="ignore")
    end = perf_counter()
    print(f"Summeries Execution time: {end - start:.2f} seconds")
    # Return JSON as string matching your original output format
    return json.dumps(json.loads(df.to_json(orient="split")), indent=4)

def pull_fault_codes(params='', headers=None):
    start = perf_counter()
    conn = http.client.HTTPSConnection('services.cat.com')
    access_token = generate_access_token()
    x_cat_api_tracking_id = generate_tracking_id()
    headers = {
    'Authorization': access_token,
    'X-Cat-API-Tracking-Id': f'{x_cat_api_tracking_id}',
    }
    params = urllib.parse.urlencode({
        'make': 'MTS'
    })
    conn.request("GET", "/catDigital/faultsHistory/v1/faults?%s" % params, headers = headers)
    response = conn.getresponse()
    raw_data = response.read()

    parsed = json.loads(raw_data)

    # Normalize into DataFrame
    df = pd.json_normalize(parsed.get("faults", []), errors="ignore")
    end = perf_counter()
    print(f"Faults Execution time: {end - start:.2f} seconds")
    # Return JSON as string matching your original output format
    return json.dumps(json.loads(df.to_json(orient="split")), indent=4)
    
conn = http.client.HTTPSConnection('services.cat.com')
try:
    conn.close()
except Exception as e:
    print(e)





