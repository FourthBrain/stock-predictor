FROM python:3.10-slim

RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

# Set the working directory to the user's home directory
WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements-core.txt .
COPY requirements-ml.txt .

# Install core dependencies with a retry mechanism
RUN for i in {1..3}; do pip install --no-cache-dir --default-timeout=600 -r requirements-core.txt && break || sleep 5; done

# Install ML libraries with a retry mechanism
RUN for i in {1..3}; do pip install --no-cache-dir --default-timeout=600 -r requirements-ml.txt && break || sleep 5; done

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
