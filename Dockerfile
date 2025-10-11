FROM python:3.13-alpine

WORKDIR /app

ADD . /app

RUN pip install pipenv && pipenv install --system && chmod +x start.sh

CMD ["./start.sh"]