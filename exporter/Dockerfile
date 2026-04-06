FROM python:3.12-slim

WORKDIR /app
COPY exporter.py /app/exporter.py

RUN pip install --no-cache-dir prometheus-client requests

EXPOSE 9200
CMD ["python", "/app/exporter.py"]
