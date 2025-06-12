# Use a slim Python 3.11 base image for smaller size
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the 'wakeonlan' utility, 'iputils-ping' for ping, and 'openssh-client' for SSH
RUN apt-get update && \
    apt-get install -y wakeonlan iputils-ping openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for SSH keys (will be mounted from host)
RUN mkdir -p /app/ssh_keys && \
    chmod 700 /app/ssh_keys

# Copy the Flask application file and static/templates directories into the container
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Expose the port that the Flask application will listen on
EXPOSE 8000

# Command to run the Flask application when the container starts
CMD ["python", "app.py"]