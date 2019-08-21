from quiz.SessionManager import Session, SessionManager
from django.views.generic import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz, Options
from django.http import HttpResponse
from quiz.serializers import QuizSerializer


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishView(View):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        # Implement PlayAgain Logic
        # View Scores
        # Save Score to Database
        return HttpResponse("YOU ARE DONE! CG!")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PlayView(View):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_random_questions() -> []:
        questions = []

        if Quiz.objects.all().count() == 0:
            return None

        quiz = Quiz.objects.all().prefetch_related('answers').order_by('?')

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
            # We have not created a valid Session for the User yet :(
            # Lets do that
            data = self.get_random_questions()
            session = Session(request.user, data)
            smngr.add_session(session)

        question_data = session.get_current_question()
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
        answer_ids = ''.join(answer_ids)
        question_id = request.POST.get('question_id')
        session = SessionManager().get_session_by_user(request.user)

        if (len(answer_ids) == 0 or answer_ids is None) or (question_id is None):
            print("ERROR!")
            return redirect('play')

        if session is None:
            print("FATAL ERROR! WTF IS GOING ON WTF WTF WTF WTF")
            return render(request, 'error.html')

        correct_answers_query = Quiz.objects.prefetch_related('answers').filter(id=question_id, answers__is_correct__exact=True)
        lewert = correct_answers_query.values('id', 'question', 'answers__id', 'answers__option', 'answers__is_correct')
        correct_answer_id = lewert[0]['answers__id']
        print("CORRECT ANSWER: {}".format(correct_answer_id))
        print("RECEIVED ANSWER: {}".format(answer_ids))

        if int(correct_answer_id) == int(answer_ids):
            print("WOOOW YOU ARE SOO GOOD ITS LIKE YOU ARE NOT SHIT")
            session = SessionManager().get_session_by_user(request.user)
            session.update_score(10)
            session.advance()

        return redirect('play')
