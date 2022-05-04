import re
from pathlib import Path

import requests

# from get_refresh_token import get_auth_token
# from document_upload import upload_document, process_response

HOST = "https://app.indico.io"
API_TOKEN_PATH = Path("/Users/fitz/Documents/api_tokens/indico_api_token.txt")

_snake_to_cc_re = re.compile(r"(.*?)_([a-zA-Z])")


def _camel(match):
    return match.group(1) + match.group(2).upper()


def snake_to_cc(string: str):
    return re.sub(_snake_to_cc_re, _camel, string, 0)


def workflow_query_builder(workflow_id, file_data):
    query = """
        mutation workflowSubmissionMutation({signature}) {{
            {mutation_name}({args}) {{
                jobIds
                submissionIds
            }}
        }}
    """

    mutation_name = "workflowSubmission"
    mutation_args = {
        "workflowId": "Int!",
        "files": "[FileInput]!",
    }
    args = [_arg for _arg in mutation_args.keys()]
    signature = ",".join(f"${_arg}: {mutation_args[_arg]}" for _arg in args)
    args = ",".join(f"{_arg}: ${_arg}" for _arg in args)
    query = query.format(mutation_name=mutation_name, signature=signature, args=args)
    variables = {
        "workflowId": workflow_id,
        "files": file_data,
        "bundle": False,
        "resultVersion": None,
    }
    return query, variables


def workflow_submission_request(auth_cookie, query, variables):
    url = f"{HOST}/graph/api/graphql"
    json_data = {"query": query, "variables": variables}
    response = requests.post(
        url, stream=True, cookies=auth_cookie, json=json_data
    )
    return response


def main(input_data):
    workflow_id = input_data["workflow_id"]
    file_data = input_data["uploaded_files"]
    refresh_token = input_data["refresh_token"]
    query, variables = workflow_query_builder(workflow_id, file_data)
    response = workflow_submission_request(refresh_token, query, variables)
    return {"response": response}

# if __name__ == "__main__":
#     with API_TOKEN_PATH.open("r") as f:
#         api_token = f.read().strip()

#     workflow_id = 3303
#     auth_cookie = get_auth_token(api_token)
    
#     filepath = Path("/Users/fitz/Downloads/sample.pdf")
#     files = upload_document(filepath, auth_cookie)
#     uploaded_files = process_response(files)
    
#     query, variables = workflow_query_builder(workflow_id, uploaded_files)
#     response = workflow_submission_request(auth_cookie, query, variables)
#     print("here")