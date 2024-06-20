# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    netcat-openbsd \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env .env
COPY wait-for-it.sh /app/wait-for-it.sh

RUN chmod +x /app/wait-for-it.sh

CMD ["sh", "-c", "/app/wait-for-it.sh db -- python manage.py collectstatic --noinput && python manage.py migrate && gunicorn nexus.wsgi:application --bind 0.0.0.0:8000"]
