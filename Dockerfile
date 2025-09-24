# Dockerfile (ETL)
FROM python:3.11-slim

# Keep python output unbuffered (useful for logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal system deps (if needed). psycopg2-binary usually doesn't need libpq devs,
# but this line is left commented if you switch to psycopg2 (source build).
# RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Ensure raw_files exists inside container
RUN mkdir -p /app/raw_files

# Run the ETL by default
ENTRYPOINT ["python", "etl_pipeline.py"]
