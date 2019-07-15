from quiz.models import *
from django.http import HttpResponse
from django.views.generic import View
from quiz.forms import PlayForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PlayView(View):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        data = {
            'id': 1,
            'question_name': 'Bist du behindert?',
            'options': ['Ja', 'Nein', 'Selber behindert!'],
            'correct_answer_id': 1
        }
        form = PlayForm(formdata=data)
        return render(request, 'play.html', {'question_name': 'Gandalf!', 'playform': form})

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
