from quiz.models import *
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz, Options
import random
from quiz.serializers import QuizSerializer


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PlayView(View):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_random_question() -> dict:
        data = {}
        if Quiz.objects.all().count() == 0:
            return None

        quiz = Quiz.objects.all().prefetch_related('answers')
        question = random.choice(quiz)

        question_data = QuizSerializer.QuizSerializer(question).data
        answers = question_data['answers']

        data['question_name'] = question_data['question']

        answers = Options.objects.filter(id__in=answers)
        data['answers'] = []
        for answer in answers:
            data['answers'].append({'answer': answer.option, 'answer_id': answer.id})

        data['question_key'] = question.id

        return data

    def get(self, request, *args, **kwargs):
        data = self.get_random_question()

        # POW!
        return render(request, 'play.html', {'data': data})

    def post(self, request, *args, **kwargs):
        """
        A dict with a crsf token is return with the keys of the questions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data: dict = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        answer_ids = request.POST.getlist('selected_answers[]')

        return redirect('play')
