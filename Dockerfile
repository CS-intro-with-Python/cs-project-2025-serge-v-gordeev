FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_RUN_RELOAD=true

CMD ["flask", "--app", "app/server.py", "run", "-h", "0.0.0.0", "-p", "8080"]