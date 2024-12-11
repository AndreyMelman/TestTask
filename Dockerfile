FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./pytest.ini /code/pytest.ini

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

EXPOSE 8000