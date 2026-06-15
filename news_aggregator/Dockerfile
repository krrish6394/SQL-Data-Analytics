ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

WORKDIR /app

# Install system build deps for some packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN chmod +x tests/run_in_container_tests.sh || true

EXPOSE 5000

CMD ["python", "app.py"]
