import logging
import requests
import os
import json

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
logger = logging.getLogger('logger')


def send_email(email, subject, htmlContent):
    """Send an email using the Brevo API."""

    try:
        logger.info(f"Email with subject:{subject} is being sent to {email}")
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        payload = {
            "sender": {
                "name": "Paperswfit",
                "email": "chandansuresh007@gmail.com"
            },
            "to": [
                {
                    "email": email
                }
            ],
            "subject": subject,
            "htmlContent": htmlContent
        }
        payload_json = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload_json)

        logger.info(f"Email with subject:{subject} sent to {email}. API Response:  {str(response.content)}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
