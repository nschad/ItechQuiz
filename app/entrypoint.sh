#!/bin/sh

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python mange.py collectstatic --no-input --clear
