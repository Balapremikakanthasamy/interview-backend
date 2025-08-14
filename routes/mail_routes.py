from flask import Blueprint, request, jsonify
from services.mail_service import send_email

mail_bp = Blueprint("mail", __name__)

@mail_bp.route("/send", methods=["POST"])
def send_mail_route():
    data = request.get_json()

    subject = data.get("subject")
    to = data.get("to")
    message = data.get("message")

    success = send_email(subject, [to], message)

    if success:
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500
