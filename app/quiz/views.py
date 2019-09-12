from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import authenticate, login

from quiz.SessionManager import Session, SessionManager
from quiz.models import Quiz, Options, HighScore
from quiz.serializers import QuizSerializer
from quiz.forms import BootsrapRegisterForm


def signup(request):
    if request.method == 'POST':
        form = BootsrapRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('play')
        else:
            form = BootsrapRegisterForm()
        return render(request, 'registration/register.html', {'form': form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishView(View):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        user = request.user
        session = SessionManager().get_session_by_user(user)

        if session and session.is_done():
            score = HighScore(score=session.score, player=user)
            score.save()
            SessionManager().close_session_by_user(user)

        highscore_data = HighScore.objects.all().order_by('-score')
        return render(request, 'finish.html', {'data': highscore_data})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReportView(View):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        data = request.session['answered_data']
        question_id = data['question_id']
        print(data)
        session = SessionManager().get_session_by_user(request.user)
        session.pop_current_question(question_id)
        options = Options.objects.filter(quiz=question_id)
        data['options'] = list(options)
        return render(request, 'report.html', {'data': data})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PlayView(View):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_random_questions() -> []:
        questions = []

        if Quiz.objects.all().count() == 0:
            return None

        quiz = Quiz.objects.all().prefetch_related('answers').order_by('?')[:15]

        for question in quiz:
            data = {}
            question_data = QuizSerializer.QuizSerializer(question).data
            answers = question_data['answers']

            data['question_name'] = question_data['question']

            answers = Options.objects.filter(id__in=answers)
            data['answers'] = []
            for answer in answers:
                data['answers'].append({'answer': answer.option, 'answer_id': answer.id})

            data['question_key'] = question.id

            questions.append(data)

        return questions

    def get(self, request, *args, **kwargs):
        smngr = SessionManager()
        session = smngr.get_session_by_user(request.user)

        if session is None:
            data = self.get_random_questions()
            session = Session(request.user, data)
            smngr.add_session(session)

        question_data = session.get_next_question()

        if question_data is None:
            return redirect('finish')
        else:
            return render(request, 'play.html', {'data': question_data})

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
        question_id = request.POST.get('question_id')
        session = SessionManager().get_session_by_user(request.user)

        answer_ids = list(map(int, answer_ids))

        if (len(answer_ids) == 0 or answer_ids is None) or (question_id is None):
            print("You have not selected anything man!")
            return redirect('play')

        if session is None:
            return render(request, 'error.html')

        correct_answers_query = Quiz.objects.prefetch_related('answers').filter(
            id=question_id,
            answers__is_correct__exact=True
        )
        lewert = correct_answers_query.values('id', 'question', 'answers__id', 'answers__option', 'answers__is_correct')
        correct_answer_ids = []
        for correct_answer in lewert:
            correct_answer_ids.append(correct_answer['answers__id'])

        if correct_answer_ids == answer_ids:
            session = SessionManager().get_session_by_user(request.user)
            session.update_score(10)
            session.advance()

        request.session['answered_data'] = {'question': Quiz.objects.get(pk=int(question_id)).question,
                                            'question_id': int(question_id), 'correct_answers': correct_answer_ids,
                                            'answered_ids': answer_ids}

        return redirect('report')
