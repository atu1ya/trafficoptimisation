FROM python:3.11-slim

RUN apt-get update && apt-get install -y sumo sumo-tools net-tools && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt pydantic-settings
COPY backend /app/backend
ENV PYTHONPATH=/app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
