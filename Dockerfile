FROM python:3.11-slim

WORKDIR /app

COPY . .

# upgrade and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements/requirements.txt

ENV HOST="0.0.0.0" \
    PORT="8000" \
    CONFIG_PATH="../config"

EXPOSE ${PORT}

# run the app
CMD ["uvicorn", "api.main:app", "--host", "${HOST}", "--port", "${PORT}"]
