import json
import atexit
from telethon.tl.types import DocumentAttributeFilename
import requests
import base64
import os
from dotenv import load_dotenv
# load_dotenv(dotenv_path="./config.env")
load_dotenv()

config = "https://raw.githubusercontent.com/Suboms/json-files/main/user_data.json"
response = requests.get(config)
if response.status_code == 200:
    user_data = json.loads(response.content.decode("utf-8"))
else:
    user_data = {}

def save_user_data(token, repo_owner, repo_name, file_path, data):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    # Load existing content of the file if it exists
    response = requests.get(url, headers=headers)
    existing_data = json.loads(response.content)["content"]
    existing_data = base64.b64decode(existing_data).decode("utf-8")
    
    # Update data with new content
    data_str = json.dumps(data, indent=4)
    data_bytes = data_str.encode("utf-8")
    data_base64 = base64.b64encode(data_bytes).decode("utf-8")

    # Commit new content
    payload = {
        "message": "Update user data",
        "content": data_base64,
        "sha": json.loads(response.content)["sha"]
    }

    response = requests.put(url, headers=headers, json=payload)
    return response

# Usage
PAT = str(os.getenv("PAT"))
REPO_OWNER = "Suboms"
REPO_NAME = "json-files"
FILE_PATH = "user_data.json"



# if user_data and isinstance(user_data, dict):
atexit.register(save_user_data, PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)

def get_user_data_from_json(user_id):
    return user_data.get(str(user_id), {})

def get_message_file_name(msg):
    if msg.file:
        if msg.media and msg.media.document:
            for attribute in msg.media.document.attributes:
                if isinstance(attribute, DocumentAttributeFilename):
                    file_name = attribute.file_name
                    file_name = file_name.replace("@TBPIndex_", "").replace("_", ".")
                    return file_name
    return ""


