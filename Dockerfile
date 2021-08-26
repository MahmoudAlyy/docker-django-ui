FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
  uwsgi \
  uwsgi-plugin-python3 

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip3 install -r requirements.txt

EXPOSE 80
