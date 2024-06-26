FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py .

# Expose the port the app runs on
EXPOSE 7860

# Run the Gradio application
CMD ["gradio", "app.py"]
