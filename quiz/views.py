from quiz.models import *
from django.http import HttpResponse
from django.views.generic import FormView
from quiz.forms import PlayForm


class PlayView(FormView):
    template_name = 'play.html'
    form_class = PlayForm
    success_url = '/play/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
