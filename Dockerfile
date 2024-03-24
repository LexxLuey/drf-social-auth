# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install python3-dev gcc libc-dev -y

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Django app
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh