FROM python:3.14-alpine

WORKDIR /app

ADD . /app

RUN apk update && apk add g++
RUN pip install pipenv && pipenv install --system && chmod +x start.sh

CMD ["./start.sh"]