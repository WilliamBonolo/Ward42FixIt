from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    reporter_cell = db.Column(db.String(10), nullable=False)
    photo_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Open', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Report {self.reference}: {self.category} - {self.status}>'

    @staticmethod
    def generate_reference():
        last_report = Report.query.order_by(Report.id.desc()).first()
        if not last_report:
            new_id = 1
        else:
            try:
                last_num = int(last_report.reference.split('-')[1])
                new_id = last_num + 1
            except (IndexError, ValueError):
                new_id = last_report.id + 1
        return f"W42-{new_id:04d}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)