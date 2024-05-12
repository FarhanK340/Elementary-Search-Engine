# Using an official Python runtime as a parent image
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /app

# Copying the current directory contents into the container at /app
COPY . /app

# Installing any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Setting environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Exposing the Flask port
EXPOSE 5000

# Running the Flask application
CMD ["flask", "run"]
