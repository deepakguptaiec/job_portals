import sqlite3
from flask import g
import hashlib

DATABASE = 'job_portal.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hash_password(password)

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Updated Users table to support 'admin', 'recruiter', 'applicant'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Create Jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                description TEXT NOT NULL,
                recruiter_id INTEGER,
                FOREIGN KEY (recruiter_id) REFERENCES users(id)
            )
        """)
        # Create Applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                applicant_id INTEGER NOT NULL,
                FOREIGN KEY (job_id) REFERENCES jobs(id),
                FOREIGN KEY (applicant_id) REFERENCES users(id)
            )
        """)
        db.commit()

        # Load sample data if tables are empty
        if not db.execute('SELECT 1 FROM users').fetchone():
            # Add sample users for all three roles
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('admin_user', hash_password('password'), 'admin','admin@gmail.com','testing'))
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('recruiter_user', hash_password('password'), 'recruiter','recruiter@gmail.com','testing'))
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('applicant_user', hash_password('password'), 'applicant','applicant@gmail.com','testing'))
            
            # Add sample job posted by recruiter_user (ID 2)
            db.execute('INSERT INTO jobs (title, company, description, recruiter_id) VALUES (?, ?, ?, ?)',
                       ('Senior Python Developer', 'TechCorp Solutions', 'Design and implement backend services using Flask and SQLite. Requires 5+ years experience.', 2))
            db.execute('INSERT INTO jobs (title, company, description, recruiter_id) VALUES (?, ?, ?, ?)',
                       ('Junior Frontend Engineer', 'InnovateX', 'Work on responsive UI development using React and Tailwind CSS. Entry-level position.', 2))
            db.commit()