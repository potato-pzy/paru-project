from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps  # Import functools for creating the login-required decorator
from routes.events import events_bp  # Import the events blueprint
from routes.academic import academic  # Import the academic blueprint
from routes.notices import notices_bp  # Import the notices blueprint
from routes.admin import admin_bp
# Initialize SQLAlchemy globally without binding to an app

db = SQLAlchemy()
app = Flask(__name__)
def create_app():
   
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with the app context
    db.init_app(app)

    # Register blueprints
 

    app.register_blueprint(admin_bp, url_prefix='/admin', name='unique_admin')
 
    app.register_blueprint(notices_bp, url_prefix='/notices', name='unique_notices')
    app.register_blueprint(academic, url_prefix='/academic', name='unique_academic')

    return app




 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Urgent/Academic/General
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class AcademicCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)


# Register Blueprints
app.register_blueprint(events_bp)  # Correctly register the events blueprint
app.register_blueprint(notices_bp, url_prefix='/notices')  # Correctly register the notices blueprint
app.register_blueprint(academic, url_prefix='/academic')


# Login-required decorator to restrict access
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('/login.html')

@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        user = User.query.filter_by(username=username).first()

        # Check credentials only if the user exists and their password is correct and they are an admin
        if user and check_password_hash(user.password, password) and user.role == 'admin':
            session['admin_logged_in'] = True
            flash("Logged in successfully!", 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')  # Flash error on failure
            return render_template('admin_login.html')  # Re-render the login page with error message

    return render_template('admin_login.html')



# Route for the admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        # Redirect back to login if not logged in
        return redirect(url_for('admin_login'))
    
    return render_template('/admin_dashboard.html')


# Route for logging out the admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Remove session data
    return redirect(url_for('admin_login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('/register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Main route - index, restricted to logged-in users only
@app.route('/')
@login_required  # Use the decorator here to enforce authentication
def index():
    return render_template('index.html')


# Protect academic and notices routes with the login_required decorator
@app.before_request
def restrict_routes():
    allowed_routes = ['login', 'register']
    if 'user_id' not in session and request.endpoint not in allowed_routes:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))



    # Create application context and initialize database
    # Application routes
app = create_app()

# Ensure database is created
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('password', method='pbkdf2:sha256')
        admin_user = User(username='admin', password=hashed_password, role='admin')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
