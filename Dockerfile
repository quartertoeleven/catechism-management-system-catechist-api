FROM python:3.13-alpine

WORKDIR /app

ADD . /app

RUN pip install pipenv && pipenv install --system

CMD ["./start.sh"]