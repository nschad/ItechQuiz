from django.db import models
from django.contrib.auth.models import User
import datetime


class Options(models.Model):
    option = models.TextField(max_length=512)
    is_correct = models.BooleanField(default=False)


class Quiz(models.Model):
    question = models.TextField(max_length=512)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE)


class HighScore(models.Model):
    score = models.IntegerField()
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    archived_at = models.DateTimeField(default=datetime.datetime.now(), blank=False)
