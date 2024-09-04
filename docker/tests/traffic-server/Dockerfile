# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Install supervisor
RUN apt-get update && apt-get install -y supervisor && apt-get install -y libpcap-dev && apt-get clean

# Copy whole project into /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the SSH and Flask ports
EXPOSE 5000

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/app/docker/tests/traffic-server/supervisord.conf"]