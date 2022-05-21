FROM python:3.7-slim

WORKDIR /cinema_django
COPY ./cinema_django .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
