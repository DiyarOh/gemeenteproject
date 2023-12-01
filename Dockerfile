# syntax=docker/dockerfile:1
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Copy requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgeos-dev

# Install GDAL
RUN apt-get update && apt-get install -y python3-gdal

# Copy your application code into the container
COPY . /code/

# Set the command to start your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]