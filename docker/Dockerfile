# Optional: containerize the 2014–2018 style stack
FROM python:3.10-slim

# System deps for Tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

# CLI entrypoint example
CMD ["python", "-m", "src.grader.cli", "--help"]
