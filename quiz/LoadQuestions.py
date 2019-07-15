from django.core.management.base import BaseCommand, CommandError
from quiz.models import Quiz, Options
import json


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        Quiz.objects.all().delete()
        Options.objects.all().delete()

        if not options['path']:
            self.stderr.write(self.style.ERROR("WTF"))

        filepath = ''.join(options['path'])
        filepath = filepath.replace('\u202a', '')

        with open(filepath, "r") as sql_data:
            data = json.loads(sql_data)
            question_list = data['questions']
            data_options = []
            data_questions = []
            for question in question_list:
                for option in question['options']:
                    temp = Options(
                        option=option,
                        is_correct=question['correct'] == option
                    )
                    data_options.append(temp)



        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
