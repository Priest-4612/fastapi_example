FROM python:3.7-slim

WORKDIR /elt_pg_to_sqlite
COPY ./elt_pg_to_sqlite .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
