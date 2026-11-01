# Ward 42 Fix-It

Ward 42 Fix-It is a Progressive Web App (PWA) built for the Mamelodi East Residents' Association. It allows residents to report community issues (like potholes, water leaks, and illegal dumping) and allows the ward coordinator to manage and track these reports.

## Features
- **Residents:** Submit reports with photos, check the status of a report using a reference number.
- **Coordinator:** Secure login, dashboard with analytics, live filtering, and the ability to update report statuses.
- **Offline Support:** Works as a PWA with an offline fallback page and local draft saving for forms.
- **Security:** CSRF protection, password hashing, strict file validation (max 2MB, specific formats), and SQL injection prevention.

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy (SQLite)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Security:** Flask-WTF (CSRF), Werkzeug (Hashing)

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WilliamBonolo/Ward42FixIt.git
   cd Ward42FixIt