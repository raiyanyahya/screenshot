FROM python:3.10-slim-bullseye


# Install required dependencies and GitHub CLI
RUN apt-get update -y && \
    apt-get install -y curl gnupg software-properties-common && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get -y update && apt-get install -y wget git
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

# Install snapsht and run setup
RUN pip install snapsht requests && snapsht setup

# Set the work directory
WORKDIR /app

# Copy the GitHub Action script
COPY entrypoint.py /app

# Set execute permissions for the entrypoint script
RUN chmod +x /app/entrypoint.py

ENTRYPOINT ["/app/entrypoint.py"]
