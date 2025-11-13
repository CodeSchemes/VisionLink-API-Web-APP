#Date: 11/12/2025 Author: William James Brown 
#Purpose: This file acts as an endpoint directory for the VisionLink api and serves formatted/pre-parsed data to the site 
#Url-Prefix set in main.py is /data/

from flask import Blueprint
from data import pull_asset_summaries, pull_fault_codes


api_routes = Blueprint("api_routes", __name__)#Parameters Blueprint(*name of file*, *always use __name__*)

@api_routes.route('/', methods=['GET'])
def index():
    data = pull_asset_summaries()
    
    return data if isinstance(data, str) else str(data)


@api_routes.route('/faults', methods=['GET'])
def faults():
    data = pull_fault_codes()
    
    return data if isinstance(data, str) else str(data)


