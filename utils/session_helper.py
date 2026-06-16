from functools import wraps
from flask import session, redirect, url_for, flash

# Simple session management (for future login feature)
def is_logged_in():
    """Check if user is logged in"""
    return session.get('logged_in', False)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def set_user_session(user_id, username):
    """Set user session data"""
    session['logged_in'] = True
    session['user_id'] = user_id
    session['username'] = username

def clear_user_session():
    """Clear user session"""
    session.clear()