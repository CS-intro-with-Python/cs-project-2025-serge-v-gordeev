FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT python3 main.py