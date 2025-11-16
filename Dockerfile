FROM python:3.12-slim

WORKDIR /app

COPY TeraBoxAPIService/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY TeraBoxAPIService/ ./TeraBoxAPIService/
COPY .env .env 2>/dev/null || true

# Expose both bot and API ports (bot doesn't use a port, but API uses 8000)
EXPOSE 8000

# Start the API server
CMD ["python", "-m", "uvicorn", "TeraBoxAPIService.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
