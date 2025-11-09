from flask import Blueprint, render_template, redirect, url_for, request, session
from .db import get_db
from .auth import login_required, role_required

bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@bp.route('/post_job', methods=['GET', 'POST'])
@login_required
@role_required('recruiter')
def post_job():
    """Recruiter can post a new job."""
    message = None
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        recruiter_id = session['user_id']
        db = get_db()

        db.execute(
            'INSERT INTO jobs (title, company, description, recruiter_id) VALUES (?, ?, ?, ?)',
            (title, company, description, recruiter_id)
        )
        db.commit()
        message = 'Success! Your job has been posted.'

    return render_template('post_job.html', message=message)

@bp.route('/job_detail/<int:job_id>')
@login_required
@role_required('recruiter')
def job_detail(job_id):
    """Recruiter views the job details and a list of applicants."""
    db = get_db()
    
    job = db.execute(
        'SELECT * FROM jobs WHERE id = ? AND recruiter_id = ?', 
        (job_id, session['user_id'])
    ).fetchone()

    if not job:
        return redirect(url_for('main.home')) 

    applicants = db.execute(
        """
        SELECT u.username, u.id AS applicant_id
        FROM applications a
        JOIN users u ON a.applicant_id = u.id
        WHERE a.job_id = ?
        """,
        (job_id,)
    ).fetchall()
    
    return render_template('job_detail.html', job=job, applicants=applicants)