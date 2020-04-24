FROM ubuntu:latest
MAINTAINER Abhishta Gatya <abhishtagatya@yahoo.com>
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip gunicorn libpq-dev
COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN pip3 install -r ./requirements.txt
ENTRYPOINT ["python3", "bot.py"]