# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_PASSWORD="thaithai" 
ENV DJANGO_SUPERUSER_USERNAME="thai"
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend/