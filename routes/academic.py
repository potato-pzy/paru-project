from flask import Blueprint, render_template

academic = Blueprint('academic', __name__)

@academic.route('/academic-calendar')
def academic_calendar():
    # Sample academic calendar data
    calendar_events = [
        {
            'month': 'January',
            'events': [
                {'date': '5th', 'description': 'Spring Semester Begins'},
                {'date': '15th', 'description': 'Last Day for Course Add/Drop'},
                {'date': '20th', 'description': 'Mid-term Exam Registration Opens'}
            ]
        },
        {
            'month': 'February',
            'events': [
                {'date': '10th', 'description': 'Midterm Examinations'},
                {'date': '14th', 'description': 'College Cultural Festival'},
                {'date': '28th', 'description': 'Research Paper Submission Deadline'}
            ]
        },
        {
            'month': 'March',
            'events': [
                {'date': '5th', 'description': 'Annual Sports Meet'},
                {'date': '15th', 'description': 'Internship Fair'},
                {'date': '25th', 'description': 'Final Semester Project Presentations'}
            ]
        },
        # Add more months as needed
    ]
    return render_template('notices/academic_calendar.html', calendar_events=calendar_events)