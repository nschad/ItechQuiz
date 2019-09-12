#!/bin/sh

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py load_questions /usr/src/app/ItechQuiz/questions.json

exec "$@"
