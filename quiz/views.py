from quiz.models import *
from django.http import HttpResponse
from django.views.generic import View
from quiz.forms import PlayForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz
import random

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PlayView(View):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        stockthingy = {
            'id': 1,
            'question_name': 'Bist du behindert?',
            'answers': ['Ja', 'Nein', 'Selber behindert!'],
            'correct_answer_id': 1
        }
        # Fetches Random Record.
        quiz = Quiz.objects.all().prefetch_related('answers')
        blub = random.choice(quiz)
        from quiz.serializers import QuizSerializer

        data = QuizSerializer.QuizSerializer(blub).data
        print(data)
        answers = blub.answers.all()
        print(answers)
        stockthingy['question_name'] = blub.question
        stockthingy['answers'] = blub.answers
        form = PlayForm(formdata=stockthingy)
        return render(request, 'play.html', {'question_name': blub.question, 'playform': form})

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
        print(data)

        return HttpResponse("DAFUQ")
