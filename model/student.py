# =========================================================
# STUDENT MODEL
# Planly - Student Workload & Task Management System
# =========================================================


class Student:
    """
    Represents a student and manages their tasks.
    """

    def __init__(self, name):
        self.name = name
        self.tasks = []

    # =====================================================
    # ADD TASK
    # =====================================================

    def add_task(self, task):
        self.tasks.append(task)

    # =====================================================
    # GET PENDING TASKS
    # =====================================================

    def get_pending_tasks(self):

        return [
            task
            for task in self.tasks
            if not task.completed
        ]

    # =====================================================
    # GET COMPLETED TASKS
    # =====================================================

    def get_completed_tasks(self):

        return [
            task
            for task in self.tasks
            if task.completed
        ]