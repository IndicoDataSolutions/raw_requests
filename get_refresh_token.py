from pathlib import Path
import requests

HOST = "https://app.indico.io"


def get_refresh_token(api_token):
    url = HOST + "/auth/users/refresh_token"
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_token}"},
    )
    return r.cookies.get_dict()

def main(input_data):
    api_token = "insert_ap_otken_here"

    refresh_token = get_refresh_token(api_token)
    print(refresh_token)
    return {"refresh_token": refresh_token["auth_token"]}
