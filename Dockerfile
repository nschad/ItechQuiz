# Python 3.7.4 with Linux Alpine
FROM python:3.7.4-alpine

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r --no-cache-dir requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]