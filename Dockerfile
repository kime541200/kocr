FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libgomp1 ffmpeg libsm6 libxext6

WORKDIR /usr/src/app

COPY . .

RUN pip install -U --force-reinstall -r requirements.txt