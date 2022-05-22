FROM python:3.9.13-slim as base

FROM base as builder

WORKDIR /install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
COPY ./elt_pg_to_sqlite/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /install/wheels -r requirements.txt

FROM base

WORKDIR /elt_pg_to_sqlite
COPY --from=builder /install/wheels /wheels
COPY --from=builder /install/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY ./elt_pg_to_sqlite .
CMD [ "python", "load_data.py" ]
