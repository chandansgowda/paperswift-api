import requests
import os
import json

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")


def send_email(email, subject, htmlContent):
    """Send an email using the Brevo API."""
    print(BREVO_API_KEY)

    try:
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

        print(response.content)
    except Exception as e:
        print(f"Failed to send email: {e}")
