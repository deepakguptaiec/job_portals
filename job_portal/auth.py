from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import wraps
from .db import get_db, hash_password, check_password
import sqlite3


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('user_role')
            required_roles = [role] if isinstance(role, str) else role
            
            if user_role not in required_roles:
                return redirect(url_for('main.home')) 
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user and check_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db = get_db()

        try:
            db.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, hash_password(password), role)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            error = 'Username already taken. Please choose a different one.'

    return render_template('register.html', error=error)

@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_role', None)
    return redirect(url_for('main.home'))