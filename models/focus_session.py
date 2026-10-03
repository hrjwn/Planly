from datetime import date, datetime

class FocusSession:

    def __init__(
        self,
        session_id,
        student_id,
        task_id,
        duration: int,
        session_date=None,
        completed: bool = True,
        subject: str = "",
        task_title: str = "",
    ):
        self.session_id = str(session_id) if session_id else None
        self.student_id = str(student_id) if student_id else None
        self.task_id = str(task_id) if task_id else None
        self.duration = int(duration) if duration else 25

        if isinstance(session_date, (datetime, date)):
            self.session_date = session_date.strftime("%Y-%m-%d")
        elif session_date:
            self.session_date = str(session_date).strip()
        else:
            self.session_date = date.today().strftime("%Y-%m-%d")

        self.completed = bool(completed)
        self.subject = subject.strip() if subject else ""
        self.task_title = task_title.strip() if task_title else ""

    def to_dict(self) -> dict:
        data = {
            "student_id": self.student_id,
            "task_id": self.task_id,
            "duration": self.duration,
            "session_date": self.session_date,
            "completed": self.completed,
            "subject": self.subject,
        }
        if self.session_id:
            data["id"] = self.session_id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            session_id=data.get("id"),
            student_id=data.get("student_id"),
            task_id=data.get("task_id"),
            duration=data.get("duration", 25),
            session_date=data.get("session_date"),
            completed=data.get("completed", True),
            subject=data.get("subject", ""),
            task_title=data.get("task_title", ""),
        )

    def __repr__(self) -> str:
        return f"<FocusSession id={self.session_id} task_id={self.task_id} duration={self.duration}m completed={self.completed}>"
