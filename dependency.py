import json
import requests
import base64
import os
from dotenv import load_dotenv
from telethon.tl.types import DocumentAttributeFilename

# Load environment variables
load_dotenv(dotenv_path="./config.env")

# Load configuration from a remote URL
def load_config_github_api(repo_owner, repo_name, file_path, pat, branch="main"):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {pat}"
    }
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()
        content_data = content.get("content")
        if content_data:
            import base64
            import json
            decoded_content = base64.b64decode(content_data).decode("utf-8")
            return json.loads(decoded_content)
    
    return {}

# GitHub API functions
def update_github_file(token, repo_owner, repo_name, file_path, data):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    response = requests.get(url, headers=headers)
    existing_data = json.loads(response.content)["content"]
    existing_data = base64.b64decode(existing_data).decode("utf-8")
    
    data_str = json.dumps(data, indent=4)
    data_bytes = data_str.encode("utf-8")
    data_base64 = base64.b64encode(data_bytes).decode("utf-8")

    payload = {
        "message": "Update user data",
        "content": data_base64,
        "sha": json.loads(response.content)["sha"]
    }

    response = requests.put(url, headers=headers, json=payload)
    return response

# Utility function to extract the file name from a message
def get_message_file_name(msg):
    if msg.file and msg.media and msg.media.document:
        for attribute in msg.media.document.attributes:
            if isinstance(attribute, DocumentAttributeFilename):
                file_name = attribute.file_name
                file_name = file_name.replace("@TBPIndex_", "").replace("_", ".")
                return file_name
    return ""

# Function to get user data from the loaded config
def get_user_data_from_json(user_id):
    return user_data.get(str(user_id), {})

# Usage


    
PAT = str(os.getenv("PAT"))
print(PAT)
REPO_OWNER = "Suboms"
REPO_NAME = "json-files"
FILE_PATH = "user_data.json"
user_data = load_config_github_api(REPO_OWNER, REPO_NAME, FILE_PATH, PAT)
print(user_data)

def save_user_data_on_exit():
    if user_data and isinstance(user_data, dict):
        update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)

    # Register the function to save data when the script exits
import atexit
atexit.register(save_user_data_on_exit)
