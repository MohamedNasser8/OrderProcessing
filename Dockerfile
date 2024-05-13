# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /usr/src/app
COPY . .

EXPOSE 80

# Define environment variable
# Run app.py when the container launches
CMD ["python", "app.py"]
