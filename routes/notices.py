from flask import Blueprint, render_template

notices_bp = Blueprint('notices', __name__)

@notices_bp.route('/notices')
def notices():
    return render_template('notices/notices.html')