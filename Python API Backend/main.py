from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@main.route('/admin')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return "Access denied", 403
    return render_template('admin_dashboard.html', name=current_user.username, users=User.query.all())