FROM python:3.11-slim

WORKDIR /app

ADD . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]