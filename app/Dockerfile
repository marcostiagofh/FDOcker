FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY init-scripts /docker-entrypoint-initdb.d/
COPY ./docker-entrypoint-initdb.d/init.sql /docker-entrypoint-initdb.d/


CMD ["python", "app.py"]
