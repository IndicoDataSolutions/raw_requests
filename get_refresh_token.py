from pathlib import Path
import requests

HOST = "https://app.indico.io"
API_TOKEN_PATH = Path("/Users/fitz/Documents/api_tokens/indico_api_token.txt")


def get_refresh_token(api_token):
    url = HOST + "/auth/users/refresh_token"
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_token}"},
    )
    return r.cookies.get_dict()

def main():
    with API_TOKEN_PATH.open("r") as f:
        api_token = f.read().strip()

    refresh_token = get_refresh_token(api_token)
    return refresh_token

if __name__ == "__main__":
    main()