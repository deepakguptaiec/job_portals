A responsive and modern Job Portal built with Python Flask, Bootstrap, and SQLite.
This project allows users to register, log in, apply for jobs, and manage job listings with role-based access.

🚀 Features
👥 User Roles
Admin — Manage all job posts and users
Recruiter — Create, update, or delete job listings
Candidate — Browse and apply for available jobs
⚙️ Core Features
User registration & login (Flask session-based authentication)
Role-based dashboard (Admin / Recruiter / Candidate)
Job posting and management system
Apply for jobs and view applied listings
Profile page with edit and update functionality
Responsive UI built with Bootstrap 5 + TailwindCSS
SQLite database for simplicity and portability
🧩 Tech Stack
Layer	Technology
Backend	Flask (Python)
Frontend	Bootstrap 5 / Tailwind CSS
Database	SQLite
Auth	Flask-Login / Flask-Session
Hosting	GitHub Pages
🗄️ Database Structure
users | id | username | email | password | role | bio |

jobs | id | title | description | company | recruiter_id |

applications | id | job_id | applied_at |

⚡️ Quick Start
# 1️⃣ Clone the repo
git clone https://github.com/deepakguptaiec/job-portals.git
cd job-portal

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the app
python run.py
