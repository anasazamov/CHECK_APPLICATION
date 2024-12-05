FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc redis && \
    apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000 5432 6379

CMD ["sh", "/app/entrypoint.sh"]
