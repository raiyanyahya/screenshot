FROM python:3.9-slim

# Install your CLI tool globally
RUN pip install snapsht

# Set the work directory
WORKDIR /app

# Download and install chrome and run snapsht setup
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo dpkg -i google-chrome-stable_current_amd64.deb
RUN snapsht setup

# Copy the GitHub Action script
COPY entrypoint.sh /app

# Set execute permissions for the entrypoint script
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]