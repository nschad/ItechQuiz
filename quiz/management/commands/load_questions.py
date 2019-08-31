import json

from django.core.management.base import BaseCommand

from quiz.models import Quiz, Options


class Command(BaseCommand):
    help = 'Loads the a JSON Formatted File (List of Questions) into the database'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        Quiz.objects.all().delete()
        Options.objects.all().delete()

        if not options['path']:
            self.stderr.write(self.style.ERROR("Please provide a valid path to a JSON Formatted Question File"))

        filepath = ''.join(options['path'])
        filepath = filepath.replace('\u202a', '')
        print(filepath)

        with open(filepath, "r", encoding="utf-8") as sql_data:
            data = json.loads(sql_data.read())
            question_list = data['questions']
            for question in question_list:
                tempQuestion = Quiz(question=question['question'])
                tempQuestion.save()
                index = question['correct']  # Int / Array
                if type(index) == int:
                    index = [index]
                for option_index, option in enumerate(question['options']):
                    temp = Options(
                        option=option,
                        is_correct=option_index in index
                    )
                    temp.save()
                    tempQuestion.answers.add(temp)

                tempQuestion.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded all Elements'))

