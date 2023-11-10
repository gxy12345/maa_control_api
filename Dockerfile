FROM python:3.9-alpine
WORKDIR /app

RUN apk update && apk add git
RUN git clone --depth 1 https://github.com/gxy12345/maa_control_api.git

WORKDIR maa_control_api

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
