FROM python:3.8.0
EXPOSE 8000

WORKDIR /usr/src/app

COPY . .

RUN apt update -qq && \
    apt upgrade -yqq && \
    apt install libgl1 -yqq

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
