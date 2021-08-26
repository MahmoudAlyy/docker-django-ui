FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip3.7 install -r requirements.txt
COPY . /code/

RUN apt-get update && apt-get install -y \
  uwsgi \
  uwsgi-plugin-python3 

#RUN cp /usr/lib/uwsgi/plugins/python3_plugin.so /code/

EXPOSE 80
