# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /social_app

# Install dependencies
COPY requirements.txt /social_app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at root
COPY . /social_app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
