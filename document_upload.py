from pathlib import Path
import json
import base64

import requests

# from get_refresh_token import get_auth_token

"""
TODO:
1) Get  auth token
2) Upload document call
3) workflow submission call
"""


HOST = "https://app.indico.io"
# API_TOKEN_PATH = Path("/Users/fitz/Documents/api_tokens/indico_api_token.txt")

def upload_document(file_content, filepath, auth_cookie):
    url = f"{HOST}/storage/files/store"
    file_data = {"files": {filepath.stem: file_content}}
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


def main(input_data):
    filepath = Path(input_data["filepath"])
    file_content = base64.b64decode(input_data["file_content"])
    refresh_token = {"auth_token": input_data["refresh_token"]}
    files = upload_document(file_content, filepath, refresh_token)
    uploaded_files = process_response(files)
    return {"uploaded_files": json.dumps(uploaded_files)}
