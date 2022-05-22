FROM python:3.9.13-slim as base

FROM base as builder

WORKDIR /install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
COPY ./cinema_django/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /install/wheels -r requirements.txt

FROM base

WORKDIR /cinema_django

COPY --from=builder /install/wheels /wheels
COPY --from=builder /install/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./cinema_django .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]

