from flask import Flask, request, Blueprint, render_template, url_for
from data import pull_asset_summaries, pull_fault_codes
from flask_cors import CORS
import pandas as pd
from api_routes import api_routes
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timezone
from flask_wtf import wtforms
from wtforms import StringField, PassowrdField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__, static_folder="../static", template_folder='../templates')
CORS(app)
app.register_blueprint(api_routes, url_prefix="/data")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config['SECRET_KEY'] = 'placeholder' #this will be in the .env file later
db = SQLAlchemy(app)



class user(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Parameters = Column(*DATA TYPE*,*KEY TRUE/FALSE*)
    fName = db.Column(db.String(20), nullable = False)
    lName = db.Column(db.String(20), nullable = False)
    username = db.Column(db.String(40), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    dateAdded = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __Repr__(self) -> str:
        return f"User {self.id}"


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def login():
    
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)