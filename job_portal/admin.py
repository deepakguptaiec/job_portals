from flask import Blueprint, render_template, redirect, url_for, request, session
from .db import get_db
from .auth import login_required, role_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    db = get_db()
    
    users = db.execute('SELECT id, username, role FROM users ORDER BY role, id').fetchall()
    
    job_count = db.execute('SELECT COUNT(*) FROM jobs').fetchone()[0]
    app_count = db.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
    
    stats = {
        'total_users': len(users),
        'job_count': job_count,
        'app_count': app_count
    }

    return render_template('admin_dashboard.html', users=users, stats=stats)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    db = get_db()
    
    if user_id == session['user_id']:
        return redirect(url_for('admin.dashboard')) 

    db.execute('DELETE FROM applications WHERE applicant_id = ?', (user_id,))
    db.execute('DELETE FROM jobs WHERE recruiter_id = ?', (user_id,))
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    
    return redirect(url_for('admin.dashboard'))