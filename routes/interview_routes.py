from flask import Blueprint, request, jsonify
from models.interview import Interview
from extensions import db, mail
from datetime import datetime, timedelta
from flask_mail import Message

interview_bp = Blueprint('interview_bp', __name__)

@interview_bp.route('/schedule', methods=['POST'])
def schedule_interview():
    data = request.json

    try:
        date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time_obj = datetime.strptime(data['time'], "%H:%M").time()
        start_dt = datetime.combine(date_obj, time_obj)
        end_dt = start_dt + timedelta(hours=1)  # default 1-hour interview

        # 🔍 Prevent double booking
        existing = Interview.query.filter_by(date=date_obj, time=time_obj).first()
        if existing:
            return jsonify({
                "error": "This time slot is already booked. Please choose another."
            }), 409

        # ✅ Save to DB
        new_interview = Interview(
            candidate_name=data['candidate_name'],
            interviewer_name=data['interviewer_name'],
            interview_type=data['interview_type'],
            date=date_obj,
            time=time_obj,
            email=data['email']
        )

        db.session.add(new_interview)
        db.session.commit()

        # 📅 Create .ics calendar invite
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Interview Scheduler//EN
BEGIN:VEVENT
UID:{new_interview.id}@interview-scheduler
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}
SUMMARY:Interview with {data['interviewer_name']}
DESCRIPTION:Interview Type: {data['interview_type']}\\nCandidate: {data['candidate_name']}
LOCATION:{data['interview_type']}
END:VEVENT
END:VCALENDAR
"""

        # 📩 Send HTML confirmation email
        subject = f"Interview Confirmation - {data['interview_type']}"
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #2d89ef;">Interview Confirmation</h2>
            <p>Hello <strong>{data['candidate_name']}</strong>,</p>
            <p>Your interview has been scheduled successfully. Here are the details:</p>
            <table style="border-collapse: collapse; margin-top: 10px;">
              <tr><td style="padding: 6px; border: 1px solid #ccc;">📅 Date</td><td style="padding: 6px; border: 1px solid #ccc;">{data['date']}</td></tr>
              <tr><td style="padding: 6px; border: 1px solid #ccc;">🕒 Time</td><td style="padding: 6px; border: 1px solid #ccc;">{data['time']}</td></tr>
              <tr><td style="padding: 6px; border: 1px solid #ccc;">👤 Interviewer</td><td style="padding: 6px; border: 1px solid #ccc;">{data['interviewer_name']}</td></tr>
              <tr><td style="padding: 6px; border: 1px solid #ccc;">💻 Type</td><td style="padding: 6px; border: 1px solid #ccc;">{data['interview_type']}</td></tr>
            </table>
            <p style="margin-top: 15px;">Please be available on time.</p>
            <p>Best regards,<br><strong>Capzora.AI Team</strong></p>
          </body>
        </html>
        """

        msg = Message(subject=subject, recipients=[data['email']])
        msg.html = html_body
        msg.attach("interview.ics", "text/calendar", ics_content)

        mail.send(msg)

        return jsonify({"message": "Interview scheduled, email with calendar invite sent!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
