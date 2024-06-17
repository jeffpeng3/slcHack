# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir aiohttp fastapi qrcode

# Copy the rest of the application code to the working directory
COPY main.py main.py

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]