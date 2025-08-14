from app import db
from datetime import datetime

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100), nullable=False)
    interviewer_name = db.Column(db.String(100), nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)  # Zoom, In-person, etc.
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "candidate_name": self.candidate_name,
            "interviewer_name": self.interviewer_name,
            "interview_type": self.interview_type,
            "date": self.date.strftime("%Y-%m-%d"),
            "time": self.time.strftime("%H:%M"),
            "email": self.email
        }
