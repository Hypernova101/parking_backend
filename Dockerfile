FROM docker.io/python:3.12

WORKDIR /home/ubuntu/parking_backend

RUN ./scripts/db_backup.py
RUN ./scripts/db_init.py
RUN ./scripts/db_restore.py

WORKDIR /

# --- [Install python and pip] ---
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip git
COPY . /

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ENV GUNICORN_CMD_ARGS="--workers=3 --bind=0.0.0.0:8000"

EXPOSE 8000

# Define environment variable
ENV FLASK_ENV=deployed

CMD [ "gunicorn", "main:app" ]
