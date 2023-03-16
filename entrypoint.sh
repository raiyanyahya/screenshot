#!/bin/bash

set -e

if [ -z "${GITHUB_TOKEN}" ]; then
  echo "GITHUB_TOKEN environment variable is not set."
  exit 1
fi

if [ -z "${INPUT_URL}" ]; then
  echo "INPUT_URL environment variable is not set."
  exit 1
fi

# Run the CLI tool to take a screenshot and save it
snapsht click "${INPUT_URL}"

# Install the GitHub CLI (gh)
apt-get update && apt-get install -y curl && apt-get clean
curl -sSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee -a /etc/apt/sources.list.d/github-cli.list
apt-get update && apt-get install -y gh

# Authenticate with the GitHub CLI
#echo "${GITHUB_TOKEN}" | gh auth login --with-token

# Post the screenshot as a comment on the PR
pr_comment="![Screenshot](data:image/png;base64,$(base64 -w0 screenshot.png))"
gh pr comment "${GITHUB_REF}" --body "$pr_comment"

# Cleanup
gh auth logout
