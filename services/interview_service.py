from models.interview import interview_store

def schedule_interview(data):
    """
    data should include:
    - candidate (str)
    - email (str)
    - datetime (str)
    - interview_type (str)
    """
    interview = {
        "candidate": data.get("candidate"),
        "email": data.get("email"),
        "datetime": data.get("datetime"),
        "interview_type": data.get("interview_type")
    }

    interview_store.append(interview)

    return {
        "success": True,
        "message": "Interview scheduled successfully"
    }
