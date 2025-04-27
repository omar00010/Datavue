FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install system dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]