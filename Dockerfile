FROM python:3.9-slim

# Install your CLI tool globally
RUN pip install snapsht

# Set the work directory
WORKDIR /app

# Copy the GitHub Action script
COPY entrypoint.sh /app

# Set execute permissions for the entrypoint script
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]