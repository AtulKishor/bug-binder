FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y \
libpq5 \
postgresql-client \
curl \
&& rm -rf /var/lib/apt/lists/*

COPY . /app
RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8000
WORKDIR /app/bugbinder
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn bugbinder.wsgi:application --bind 0.0.0.0:8000"]