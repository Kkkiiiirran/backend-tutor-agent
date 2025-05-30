# Use official Python slim image
FROM python:3.12-slim

# Install system dependencies including python3-tk for tkinter support
RUN apt-get update && apt-get install -y python3-tk && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose port your app runs on (default 8000 for uvicorn)
EXPOSE 8000

# Start the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
