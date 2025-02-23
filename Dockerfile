# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the current directory contents into the container
COPY . .

# Make port 5000 available to the world outside this container
EX
POSE 5000/

# Run app.py when the container launches. Adjust this path if app.py resides in a different location.
CMD ["python", "./app.py"]
