#!/usr/bin/env python3

import os
import json
import base64
import requests
from subprocess import call

def main():
    # Add safe.directory configuration to git
    call(["git", "config", "--global", "--add", "safe.directory", "/github/workspace"])

    # Take a screenshot using the snapsht CLI tool
    call(["snapsht", "click", os.environ["INPUT_URL"]])

    # Get the pull request number from the GitHub Actions event payload
    with open(os.environ["GITHUB_EVENT_PATH"]) as event_file:
        event_data = json.load(event_file)
        pr_number = event_data["number"]

    # Authenticate the GitHub CLI using the provided GITHUB_TOKEN
    #call(["gh", "auth", "login", "--with-token"], input=os.environ["GITHUB_TOKEN"].encode(), text=True)

    # Upload the screenshot to GitHub using the API
    upload_url = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = { "body": "Uploading screenshot..." }
    response = requests.post(upload_url, headers=headers, json=data)
    comment_id = response.json()["id"]

    # Upload the image to the comment
    attachment_url = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/issues/comments/{comment_id}/attachments"
    headers = {
         "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Content-Type": "image/png",
        #"Content-Type": "text/markdown; charset=UTF-8",
        #"Content-Disposition": "attachment;filename=screenshot.png"
    }
    for entry in os.scandir('.'):
        if entry.is_file():
            print(entry.name)
    with open("screenshot.png", "rb") as image_file:
        image_data = image_file.read()
    response = requests.post(attachment_url, headers=headers, data=image_data, auth=("user", os.environ["GITHUB_TOKEN"]))

    # Edit the comment to include the uploaded image
    call(["gh", "pr", "comment", str(pr_number), "--edit-last", "--body", "![Screenshot](attachment://screenshot.png)"])

    # Logout from GitHub CLI
    #call(["gh", "auth", "logout"])


if __name__ == "__main__":
    main()
