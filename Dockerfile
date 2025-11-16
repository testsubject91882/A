FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY TeraBoxAPIService/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY TeraBoxAPIService/ ./TeraBoxAPIService/

# Expose API port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "TeraBoxAPIService.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
