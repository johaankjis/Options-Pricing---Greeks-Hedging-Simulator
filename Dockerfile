# Dockerfile for containerized deployment
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY pricing.py .
COPY pricing_optimized.py .
COPY validation.py .
COPY hedging.py .
COPY dashboard.py .
COPY scripts/ scripts/

# Expose dashboard port
EXPOSE 8050

# Run dashboard by default
CMD ["python", "scripts/run_dashboard.py"]
