FROM python:3.11.8-slim-bookworm

RUN pip install --no-cache --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache -r /requirements.txt

COPY ./app/ /app/
COPY ./.env/ /.env/

WORKDIR /app

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]