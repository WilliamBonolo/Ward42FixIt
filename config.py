import os

class Config:
    # Security: Change this to a long random string in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-ward42-fixit'
    
    # Database setup (SQLite)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'fixit.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Settings (Part E requirement)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}