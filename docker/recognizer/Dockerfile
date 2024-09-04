FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Copy the Python script and requirements.txt into the container
COPY docker/recognizer/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project into /app
COPY . /app

# Command to run the Python client
CMD ["python", "scripts/start_default_recognizer.py"]
