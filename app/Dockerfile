# Python 3.7.4 with Linux Alpine
FROM python:3.7.4-alpine

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
