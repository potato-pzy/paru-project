from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
 
# Create a Blueprint for admin routes
admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates')

# Admin Dashboard Route
@admin_bp.route('/dashboard')
def admin_dashboard():
    from app import Notice, Event, AcademicCalendar, db
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_bp.admin_login'))

    # Fetch all notices, events, and calendar events from the database
    notices = Notice.query.all()
    events = event.query.all()
    calendar_events = academicCalendar.query.all()
    

    return render_template(
        'admin_dashboard.html',
        notices=notices,
        events=events,
        calendar_events=calendar_events
    )

# Add Notice
@admin_bp.route('/add_notice', methods=['POST'])
def add_notice():
    title = request.form['title']
    category = request.form['category']
    description = request.form['description']
    from app import Notice, Event, AcademicCalendar, db

    new_notice = Notice(title=title, category=category, content=description)
    db.session.add(new_notice)
    db.session.commit()
    flash('Notice added successfully!', 'success')

    return redirect(url_for('admin_bp.admin_dashboard'))

# Add Event
@admin_bp.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    description = request.form['description']
    from app import Notice, Event, AcademicCalendar, db

    new_event = Event(title=title, date=datetime.strptime(date, '%Y-%m-%d'), description=description)
    db.session.add(new_event)
    db.session.commit()
    flash('Event added successfully!', 'success')

    return redirect(url_for('admin_bp.admin_dashboard'))

# Add Calendar Event
@admin_bp.route('/add_calendar_event', methods=['POST'])
def add_calendar_event():
    month = request.form['month']
    date = request.form['date']
    description = request.form['description']
    from app import Notice, Event, AcademicCalendar, db

    new_calendar_event = AcademicCalendar(
        month=month,
        date=datetime.strptime(date, '%Y-%m-%d'),
        description=description
    )
    db.session.add(new_calendar_event)
    db.session.commit()
    flash('Calendar event added successfully!', 'success')

    return redirect(url_for('admin_bp.admin_dashboard'))

# Admin Login Route
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Assuming User model is already defined with admin roles
        from models import User
        user = User.query.filter_by(username=username).first()

        if user and user.role == 'admin' and user.check_password(password):
            session['admin_logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_bp.admin_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('admin_login.html')

# Admin Logout
@admin_bp.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_bp.admin_login'))
