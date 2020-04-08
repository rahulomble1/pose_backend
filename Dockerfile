FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update
RUN apt -y install python3.8
RUN apt install -y ffmpeg
RUN apt-get install -y frei0r-plugins
RUN apt-get update
RUN apt-get -y install python3-pip

RUN mkdir pose_backend

COPY . /pose_backend

WORKDIR /pose_backend

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3","app.py"]






#
#
## set the base image
#FROM python:3.6
##add project files to the usr/src/app folder
#ADD . /app
##set directoty where CMD will execute
#WORKDIR /app
#
#
## Get pip to download and install requirements:
#RUN pip install --no-cache-dir -r requirements.txt
#
## run the command to start uWSGI
#
#CMD ["uwsgi", "app.ini"]

