#!/usr/bin/env python3

import os
import sys
import json
from subprocess import call
import dropbox

def main(url, dropbox_token):
    call(["git", "config", "--global", "--add", "safe.directory", "/github/workspace"])
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
        meta = dbx.files_upload(image_file.read(), f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png", mode=dropbox.files.WriteMode("overwrite"))
        print(meta)
    
    # Check the account type
    account = dbx.users_get_current_account()
    is_team_account = account.account_type.is_team()

    # Prepare the shared link settings based on the account type
    if is_team_account:
        shared_link_settings = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.team_only)
    else:
        shared_link_settings = None

    # Try to create a shared link, and if it already exists, use the existing link
    try:
        if shared_link_settings:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png", shared_link_settings)
        else:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png")
        shared_link = shared_link_metadata.url
        dropbox_link = shared_link.replace('?dl=0', '?dl=1')
    except dropbox.exceptions.ApiError as e:
        if e.error.is_shared_link_already_exists():
            shared_link_metadata = dbx.sharing_get_shared_links(f"/screenshots/{os.environ['GITHUB_REPOSITORY']}_PR_{pr_number}.png")
            shared_link = shared_link_metadata.links[0].url
            dropbox_link = shared_link.replace('?dl=0', '?dl=1')
        else:
            raise

    comment_body = f"Screenshot uploaded to Dropbox: [View Screenshot]({dropbox_link})"
    call(["gh", "pr", "comment", str(pr_number), "--edit-last", "--body", comment_body])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: entrypoint.py <url> <dropbox_token>")
        sys.exit(1)
    
    url = sys.argv[1]
    dropbox_token = sys.argv[2]
    main(url, dropbox_token)