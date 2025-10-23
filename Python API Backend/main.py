from flask import Flask, request
from data import pull_asset_summaries, pull_fault_codes
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    data = pull_asset_summaries()
    
    return data if isinstance(data, str) else str(data)

@app.route('/faults', methods=['GET'])
def faults():
    data = pull_fault_codes()
    
    return data if isinstance(data, str) else str(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)