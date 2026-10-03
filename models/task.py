from datetime import date, datetime
from typing import Optional


class Task:

    VALID_PRIORITIES = ["Low", "Medium", "High"]

    def __init__(
        self,
        task_id,
        student_id,
        title: str,
        subject: str,
        deadline,
        priority: str = "Medium",
        completed: bool = False,
    ):
        self.task_id = str(task_id) if task_id else None
        self.student_id = str(student_id) if student_id else None
        self.title = title.strip() if title else ""
        self.subject = subject.strip() if subject else ""

        if isinstance(deadline, (datetime, date)):
            self.deadline = deadline.strftime("%Y-%m-%d")
        elif deadline:
            self.deadline = str(deadline).strip()
        else:
            self.deadline = date.today().strftime("%Y-%m-%d")

        clean_priority = priority.strip().capitalize() if priority else "Medium"
        self.priority = clean_priority if clean_priority in self.VALID_PRIORITIES else "Medium"

        self.completed = bool(completed)

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def is_completed(self) -> bool:
        return self.completed

    def update_details(
        self,
        title: str,
        subject: str,
        deadline,
        priority: str,
        completed: bool = None,
    ):
        if title:
            self.title = title.strip()
        if subject:
            self.subject = subject.strip()
        if deadline:
            if isinstance(deadline, (datetime, date)):
                self.deadline = deadline.strftime("%Y-%m-%d")
            else:
                self.deadline = str(deadline).strip()
        if priority:
            clean_priority = priority.strip().capitalize()
            if clean_priority in self.VALID_PRIORITIES:
                self.priority = clean_priority
        if completed is not None:
            self.completed = bool(completed)

    def deadline_date(self) -> Optional[date]:
        try:
            return datetime.strptime(self.deadline, "%Y-%m-%d").date()
        except Exception:
            return None

    def days_until_deadline(self) -> int:
        due_date = self.deadline_date()
        if due_date is None:
            return 999
        return (due_date - date.today()).days

    def is_overdue(self) -> bool:
        return not self.completed and self.days_until_deadline() < 0

    def to_dict(self) -> dict:
        data = {
            "student_id": self.student_id,
            "title": self.title,
            "subject": self.subject,
            "deadline": self.deadline,
            "priority": self.priority,
            "completed": self.completed,
        }
        if self.task_id:
            data["id"] = self.task_id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            task_id=data.get("id"),
            student_id=data.get("student_id"),
            title=data.get("title", ""),
            subject=data.get("subject", ""),
            deadline=data.get("deadline", ""),
            priority=data.get("priority", "Medium"),
            completed=data.get("completed", False),
        )

    def __repr__(self) -> str:
        status_str = "Done" if self.completed else "Pending"
        return f"<Task id={self.task_id} title='{self.title}' priority={self.priority} status={status_str}>"