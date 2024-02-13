import secrets
import time

def generate_random_token():
    timestamp = int(time.time() * 1000)
    random_component = secrets.token_urlsafe(16)
    token = f"{timestamp}-{random_component}"
    return token