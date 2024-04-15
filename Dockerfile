FROM python:3

WORKDIR /lms_app

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt

COPY . .
