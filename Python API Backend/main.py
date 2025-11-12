from flask import Flask, request, Blueprint, render_template
from data import pull_asset_summaries, pull_fault_codes
from flask_cors import CORS
import pandas as pd
from api_routes import api_routes


app = Flask(__name__, static_folder="../static", template_folder='../templates')
CORS(app)
app.register_blueprint(api_routes, url_prefix="/data")

@app.route('/', methods=['GET'])
def index():
    
    return render_template("index.html")


@app.route('/sign_in', methods=['GET'])
def sign_in():
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)