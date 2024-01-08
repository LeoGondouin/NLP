# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./db/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./db /app

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Define environment variable
ENV NAME db_api

# Run api.py when the container launches
CMD ["python", "api.py"]
