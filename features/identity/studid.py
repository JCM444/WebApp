import requests

API_URL = "https://api.studid.io/v2/auth/verification"

def create_verification(secret_token, redirect_url):
    response = requests.post(
        API_URL,
        json={
            "secretToken": secret_token,
            "redirectUrl": redirect_url,
            "serviceName": "Study Circle"
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()
    
def get_verification(verification_id, secret_token):
    response = requests.get(
        f"{API_URL}/{verification_id}",
        headers={
            "Authorization": f"Bearer {secret_token}"
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()
