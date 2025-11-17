#------------------------------------------------------------------------------------------------------------Imports------------------------------------------------------------------------------------------------------------

from flask import Flask, request, Blueprint, render_template, url_for, redirect, session
from data import pull_asset_summaries, pull_fault_codes
from flask_cors import CORS
import pandas as pd
from api_routes import api_routes
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

#------------------------------------------------------------------------------------------------------------Config------------------------------------------------------------------------------------------------------------

app = Flask(__name__, static_folder="../static", template_folder='../templates')
CORS(app)
app.register_blueprint(api_routes, url_prefix="/data")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config['SECRET_KEY'] = 'placeholder' #this will be in the .env file later as an actual key
db = SQLAlchemy(app)

#------------------------------------------------------------------------------------------------------------User Models------------------------------------------------------------------------------------------------------------

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Parameters = Column(*DATA TYPE*,*KEY TRUE/FALSE*)
    username = db.Column(db.String(40), nullable = False, unique = True)
    password_hash = db.Column(db.String(255), nullable = False)
    dateAdded = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"Task {self.id}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()


#------------------------------------------------------------------------------------------------------------Routes------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if "username" in session and session["username"] == "admin":
        print("Admin login achieved")
        return redirect(url_for('admin'))
    elif "username" in session:
        print("User session found")
        return render_template("dashboard.html")
    else:
        return render_template("index.html")

#------------------------------------------------------------------------------------------------------------
@app.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template("dashboard.html")

#------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":
        print("Post Login Reached")
        username = request.form["uname"]
        password = request.form["psw"]
        print("Credentials Receieved")
        User = user.query.filter_by(username=username).first()
        if User and User.check_password(password):
            print("User found")
            session['username'] = username
            print(username)
            print(password)
            return redirect(url_for('dashboard'))
        else:
            print("Rendering index")
            print(User)
            
            return render_template('index.html', error='Invalid username or password.')

        
    else:
        print("Get Login Reached")
        return render_template("login.html")
    
#------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        print("Reached Post Register")
        print("Credentials Recieved")
        username = request.form["uname"]
        password = request.form["psw"]
        print(username)
        print(password)

        existing_user = user.query.filter_by(username=username).first()
        if existing_user:
            print("User session exists")
            return render_template('index.html', error='Username already exists.')
        else:
            print("Credentials commited to database")
            new_user = user(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('dashboard'))
            
    else:
        print("Reached Get Register")
        return render_template("register.html")
    
#------------------------------------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#------------------------------------------------------------------------------------------------------------

@app.route("/admin")
def admin():
        
        users = user.query.order_by(user.username).all()
        return render_template("adminPage.html", users = users)

#------------------------------------------------------------------------------------------------------------
#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_user = user.query.get_or_404(id)
    try:
        db.session.delete(delete_user)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"
    
#------------------------------------------------------------------------------------------------------------

@app.route("/update/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    User = user.query.get_or_404(id)
    if request.method == "POST":
        User.username = request.form['username']
        new_password = request.form['password']
        User.set_password(new_password)
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR {e}"
        
    else:
        return render_template('edit.html', User=User)
#------------------------------------------------------------------------------------------------------------Running Loop------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)