class Student:

    def __init__(self, student_id, auth_user_id, name: str, email: str, course: str):
        self.student_id = str(student_id) if student_id else None
        self.auth_user_id = str(auth_user_id) if auth_user_id else None
        self.name = name.strip() if name else ""
        self.email = email.strip().lower() if email else ""
        self.course = course.strip() if course else ""

    def update_info(self, name: str, course: str):
        if name:
            self.name = name.strip()
        if course:
            self.course = course.strip()

    def to_dict(self) -> dict:
        data = {
            "auth_user_id": self.auth_user_id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
        }
        if self.student_id:
            data["id"] = self.student_id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data.get("id"),
            auth_user_id=data.get("auth_user_id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            course=data.get("course", ""),
        )

    def __repr__(self) -> str:
        return f"<Student id={self.student_id} name='{self.name}' course='{self.course}'>"