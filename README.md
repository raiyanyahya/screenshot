# screenshot
This GitHub Action takes a screenshot of a given URL, uploads it to Dropbox and posts the image url as a comment on the associated pull request. It's useful for visualizing changes in a UI project, previewing a deployed staging environment, or any situation where a visual representation of the changes in a PR is helpful.

## Prerequisites
To use this action, you must have the following:

A GitHub repository with a workflow that triggers on pull request events and a DropBox Access Token.

## Usage
To use this action in your workflow, follow these steps:

1.Navigate to the GitHub Marketplace and search for "Screenshot Action" or visit the action's GitHub Marketplace page directly.

2.Click the "Use latest version" button to add the action to your repository.

3.In your repository, create a .github/workflows directory if it doesn't already exist.

4.Add a new workflow file, e.g., screenshot_on_pr.yml.

5Include the following example workflow in your new file, replacing your-username with the action creator's GitHub username and https://example.com with the desired URL to capture a screenshot of:

```
name: Screenshot on PR

on:
  pull_request:
    types:
      - opened
      - synchronize

jobs:
  screenshot:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Take screenshot and post it on the PR
      uses: your-username/screenshot-action@master
      with:
        url: 'https://example.com'
        dropbox_token: ${{ secrets.DROPBOX_TOKEN }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
This example workflow runs on pull request events with opened and synchronize types. It checks out the repository, captures a screenshot using the snapsht CLI tool, uploads it to DropBox and posts the image url as a comment on the pull request.

## Configuration
Currently, this action takes a single required input:

url: The URL to capture a screenshot of.
The GITHUB_TOKEN environment variable is also required and should be set to ${{ secrets.GITHUB_TOKEN }} to use the default token provided by GitHub Actions.
The DROPBOX_TOKEN is stored as a repository secret.

## Contributing
Contributions to this project are welcome! Please feel free to open issues or submit pull requests with bug fixes, improvements, or new features.

## License
This project is licensed under the MIT License.
