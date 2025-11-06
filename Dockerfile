FROM python:3.14-alpine

WORKDIR /app

ADD . /app

RUN pip install pipenv && pipenv install --system && chmod +x start.sh

CMD ["./start.sh"]