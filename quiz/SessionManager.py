from typing import Optional, Any
from django.contrib.auth.models import User


class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class Session:
    def __init__(self, username: User, questions: []):
        self.score = 0
        self.username: User = username
        self.current_question_idx = 0
        self.questions: [] = questions

    def update_score(self, score):
        self.score += score

    def get_questions(self) -> []:
        return self.questions

    def get_current_question(self) -> Optional[str]:
        if self.current_question_idx > len(self.questions):
            return None
        else:
            return self.questions[self.current_question_idx]

    def advance(self):
        self.current_question_idx += 1


class SessionManager(Singleton):

    def init(self, *args, **kwds):
        self.sessions: [User] = []

    def add_session(self, session: Session):
        self.sessions.append(session)

    def get_session_by_user(self, username: User) -> Optional[Session]:
        for session in self.sessions:
            if session.username == username:
                return session
        return None

    def close_session_by_user(self, username: User):
        for session in self.sessions:
            if session.user == username:
                self.sessions.remove(session)
