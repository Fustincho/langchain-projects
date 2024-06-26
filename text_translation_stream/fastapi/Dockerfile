FROM python:3.12-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]