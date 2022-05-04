from contextlib import contextmanager
from pathlib import Path
import json

import requests

# from get_refresh_token import get_refresh_token

"""
TODO:
1) Get  auth token
2) Upload document call
3) workflow submission call
"""


HOST = "https://app.indico.io"
API_TOKEN_PATH = Path("/Users/fitz/Documents/api_tokens/indico_api_token.txt")

@contextmanager
def handle_file(filepath):
    f = filepath.open("rb")
    file_dict = {"files": {filepath.stem: f}}
    yield file_dict
    f.close()


def upload_document(filepath, auth_cookie):
    url = f"{HOST}/storage/files/store"
    with handle_file(filepath) as file_data:
        response = requests.post(
            url,
            stream=True,
            cookies=auth_cookie,
            **file_data,
        )
    return response.json()


def process_response(uploaded_files):
    files = [
        {
            "filename": f["name"],
            "filemeta": json.dumps(
                {
                    "path": f["path"],
                    "name": f["name"],
                    "uploadType": f["upload_type"],
                }
            ),
        }
        for f in uploaded_files
    ]
    return files


def main(input):
    filepath = input["filepath"]
    refresh_token = input["refresh_token"]
    files = upload_document(filepath, refresh_token)
    uploaded_files = process_response(files)
    return {"uploaded_files": uploaded_files}


# if __name__ == "__main__":
#     with API_TOKEN_PATH.open("r") as f:
#         api_token = f.read().strip()

#     refresh_token = get_refresh_token(api_token)
#     filepath = Path("/Users/fitz/Downloads/sample.pdf")
#     input_data = {
#         "refresh_token": refresh_token,
#         "filepath": filepath
#     }
#     main(input_data)
