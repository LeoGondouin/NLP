# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./scraper/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./scraper /app

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV NAME scraping_api

# Run api.py when the container launches
CMD ["python", "api.py"]
