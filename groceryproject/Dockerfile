# Start with a base Python image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED  1

# Set work directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose the port that your app runs on
EXPOSE  8000

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
