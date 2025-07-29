# Start with Python runtime
FROM python:3.10-slim

# Set up workspace
WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
