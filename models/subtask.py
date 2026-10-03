class Subtask:
    """A specific step that works toward finishing a main Task."""

    def __init__(
        self,
        subtask_id,
        task_id,
        student_id,
        title: str,
        completed: bool = False,
        position: int = 0,
    ):
        self.subtask_id = str(subtask_id) if subtask_id else None
        self.task_id = str(task_id) if task_id else None
        self.student_id = str(student_id) if student_id else None
        self.title = title.strip() if title else ""
        self.completed = bool(completed)
        self.position = int(position) if position else 0

    def to_dict(self) -> dict:
        data = {
            "task_id": self.task_id,
            "student_id": self.student_id,
            "title": self.title,
            "completed": self.completed,
            "position": self.position,
        }
        if self.subtask_id:
            data["id"] = self.subtask_id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            subtask_id=data.get("id"),
            task_id=data.get("task_id"),
            student_id=data.get("student_id"),
            title=data.get("title", ""),
            completed=data.get("completed", False),
            position=data.get("position", 0),
        )

    def __repr__(self) -> str:
        status_str = "Done" if self.completed else "Pending"
        return f"<Subtask id={self.subtask_id} task={self.task_id} title='{self.title}' status={status_str}>"
