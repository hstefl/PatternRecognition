# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /webapp
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project into /app
COPY . /app

# Port 5000 is intended to exposes to access webapp
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app/webapp/pattern-recognition.py

# Run webapp.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
