from typing import Optional

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
        self.questions: [dict] = questions
        self.answered = {}

    def update_score(self, score):
        self.score += score

    def get_questions(self) -> []:
        return self.questions

    def is_done(self) -> bool:
        return len(self.questions) == 0

    def set_answered(self, question_id: str, options_ids: []):
        self.answered = {'question_id': question_id, 'options_ids': options_ids}

    def get_next_question(self) -> Optional[dict]:
        try:
            return self.questions[0]
        except IndexError:
            return None
        except TypeError:
            return None

    def pop_current_question(self, id: int):
        for question in self.questions:
            if question['question_key'] == id:
                self.questions.remove(question)

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
            if session.username == username:
                self.sessions.remove(session)
