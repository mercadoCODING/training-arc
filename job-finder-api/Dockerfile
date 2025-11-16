FROM python:3.11-slim

WORKDIR /app

#Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

#Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Download sentence transformer model during build (saves time on startup)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')"

#Copy application code
COPY main.py .

#Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

#expose port
EXPOSE 8080

#Run FastAPI with uvicorn
CMD exec uvicorn job_matcher_api:app --host 0.0.0.0 --port ${PORT} --workers 1