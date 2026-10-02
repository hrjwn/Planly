# =========================================================
# PLANLY APPLICATION CLASS
# Planly - Student Workload & Task Management System
# =========================================================

from backend.model import Task, Student
from backend.services import WorkloadAnalyzer, StudyScheduler


class PlanlyApp:

    def __init__(self):
        self.student = Student("Student")
        self.analyzer = WorkloadAnalyzer()
        self.scheduler = StudyScheduler()

    def add_task(
        self,
        name,
        subject,
        priority,
        deadline,
        estimated_hours
    ):

        task = Task(
            name,
            subject,
            priority,
            deadline,
            estimated_hours
        )

        self.student.add_task(task)

    def complete_task(self, task_index):

        if 0 <= task_index < len(
            self.student.tasks
        ):

            self.student.tasks[
                task_index
            ].mark_completed()

            return True

        return False
