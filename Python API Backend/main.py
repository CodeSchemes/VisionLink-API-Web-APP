from flask import Flask, request, Blueprint, render_template, url_for, redirect, session
from data import pull_asset_summaries, pull_fault_codes
from flask_cors import CORS
import pandas as pd
from api_routes import api_routes
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="../static", template_folder='../templates')
CORS(app)
app.register_blueprint(api_routes, url_prefix="/data")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config['SECRET_KEY'] = 'placeholder' #this will be in the .env file later as an actual key
db = SQLAlchemy(app)



class user(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Parameters = Column(*DATA TYPE*,*KEY TRUE/FALSE*)
    fName = db.Column(db.String(20), nullable = False)
    lName = db.Column(db.String(20), nullable = False)
    username = db.Column(db.String(40), nullable = False, unique = True)
    password_hash = db.Column(db.String(255), nullable = False)
    dateAdded = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __Repr__(self) -> str:
        return f"User {self.id}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    
    return render_template("index.html")

@app.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template("dashboard.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":
        username = request.form("uname")
        password = request.form("psw")

    else:
        return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":
        fName = request.form("fName")
        lName = request.form("lName")
        password = request.form("psw")

        #create username out of first and last name Ex. -> John Doe === jdoe
        #if jdoe already exists add a numeral 2-10
        firstInitial = fName[0]
        username = f"{firstInitial.toLower()}{lName.toLower()}"

        #encrypt password here function

            
            
    else:

        return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)