class Session:
    def __init__(self, user, session_id, questions: []):
        self.score = 0
        self.user = user
        self.current_question_idx = 0
        self.session_id = session_id
        self.questions: [] = questions

    def update_score(self, score):
        self.score += score

    def get_questions(self) -> []:
        return self.questions

    def get_current_question(self) -> str:
        if self.current_question_idx > len(self.questions):
            return None
        else:
            return self.questions[self.current_question_idx]

    def advance(self):
        self.current_question_idx += 1


class SessionManager:

    def __init__(self):
        self.sessions: [Session] = []

    def add_session(self, session: Session):
        self.sessions.append(session)

    def get_session(self, session_id: str):
        for session in self.sessions:
            if session.session_id == session_id:
                return session

    def close_session(self, session_id: str):
        for session in self.sessions:
            if session.session_id == session_id:
                self.sessions.remove(session)
