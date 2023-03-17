#!/usr/bin/env python3

import os
import sys
import json
from subprocess import call
import dropbox

def main(url, dropbox_token):
    # Take a screenshot using the snapsht CLI tool
    call(["snapsht", "click", url])
    print(url)
    # Get the pull request number from the GitHub Actions event payload
    with open(os.environ["GITHUB_EVENT_PATH"]) as event_file:
        event_data = json.load(event_file)
        pr_number = event_data["number"]

    # Authenticate Dropbox and upload the screenshot
    dbx = dropbox.Dropbox(dropbox_token)
    with open("screenshot.png", "rb") as image_file:
        dbx.files_upload(image_file.read(), f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png", mode=dropbox.files.WriteMode("overwrite"))

    # Send a PR comment with the Dropbox link
    dropbox_link = dbx.sharing_create_shared_link_with_settings(f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png").url
    comment_body = f"Screenshot uploaded to Dropbox: [View Screenshot]({dropbox_link})"
    call(["gh", "pr", "comment", str(pr_number), "--edit-last", "--body", comment_body])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: entrypoint.py <url> <dropbox_token>")
        sys.exit(1)
    
    url = sys.argv[1]
    dropbox_token = sys.argv[2]
    main(url, dropbox_token)