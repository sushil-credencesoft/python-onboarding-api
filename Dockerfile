# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# RUN python -m venv venv

# RUN ./venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variable (default to TEST, override with `docker run -e`)
ENV env_variable=TEST

EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
