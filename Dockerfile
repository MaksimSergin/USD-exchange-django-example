FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

USER appuser

COPY . /app/

EXPOSE 8000
