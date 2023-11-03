FROM python:3.9-alpine
WORKDIR /app

RUN apk update && apk add git
RUN git clone --depth 1 https://gitlab.com/gxy12345/genshin-checkin-helper.git

WORKDIR genshin-checkin-helper

RUN pip install --no-cache-dir -r requirements.txt