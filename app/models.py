from datetime import datetime
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