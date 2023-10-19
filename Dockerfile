FROM python:3.10-slim

RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

# Set the working directory to the user's home directory
WORKDIR /app

RUN pip install --no-cache-dir -U pip

COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]