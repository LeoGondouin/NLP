# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Define environment variable
ENV NAME dash_app

# Run app.py when the container launches
CMD ["python", "app.py"]
