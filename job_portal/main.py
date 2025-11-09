from flask import Blueprint, render_template, redirect, url_for, request,jsonify, session, g
from .db import get_db
from .auth import login_required, role_required

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    """Displays the list of all available jobs."""
    db = get_db()
    # Fetch job list
    jobs = db.execute('SELECT * FROM jobs ORDER BY id DESC').fetchall()
    
    # Check current user's applied status if logged in as applicant
    applied_job_ids = set()
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    if user_role == 'recruiter' and user_id:
        jobs = db.execute('SELECT * FROM jobs where recruiter_id = ? ORDER BY id DESC',(user_id,)).fetchall()
        
    if user_role == 'applicant' and user_id:
        applications = db.execute(
            'SELECT job_id FROM applications WHERE applicant_id = ?', (user_id,)
        ).fetchall()
        applied_job_ids = {app['job_id'] for app in applications}

    return render_template('home.html', jobs=jobs, applied_job_ids=applied_job_ids)

@bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
@role_required('applicant')
def apply(job_id):
    """Applicant applies for a specific job."""
    applicant_id = session['user_id']
    db = get_db()

    # Check for existing application
    existing = db.execute(
        'SELECT * FROM applications WHERE job_id = ? AND applicant_id = ?',
        (job_id, applicant_id)
    ).fetchone()

    if not existing:
        db.execute(
            'INSERT INTO applications (job_id, applicant_id) VALUES (?, ?)',
            (job_id, applicant_id)
        )
        db.commit()
    
    return redirect(url_for('main.home'))

@bp.route('/my_applications')
@login_required
@role_required('applicant')
def my_applications():
    """Displays jobs the applicant has applied for."""
    applicant_id = session['user_id']
    db = get_db()

    applications = db.execute(
        """
        SELECT j.title, j.company, j.description, j.id
        FROM jobs j
        JOIN applications a ON j.id = a.job_id
        WHERE a.applicant_id = ?
        ORDER BY j.id DESC
        """,
        (applicant_id,)
    ).fetchall()

    return render_template('my_applications.html', applications=applications)


@bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']

    db = get_db()
    user_data = db.execute(
        """
        SELECT * FROM users WHERE id = ?
        """,
        (user_id,)
    ).fetchone()
    return render_template('profile.html', user_data=user_data)

@bp.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    db = get_db()
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    bio = data.get("bio")

    # Update user info
    db.execute(
        "UPDATE users SET username = ?, email = ?, bio = ? WHERE id = ?",
        (name, email, bio, user_id)
    )
    db.commit()

    return jsonify({"success": True, "message": "Profile updated successfully!"})