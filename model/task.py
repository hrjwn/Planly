# =========================================================
# TASK MODEL
# Planly - Student Workload & Task Management System
# =========================================================


class Task:
    """
    Represents an academic task in Planly.
    """

    def __init__(
        self,
        name,
        subject,
        priority,
        deadline,
        estimated_hours
    ):
        self.name = name
        self.subject = subject
        self.priority = priority
        self.deadline = deadline
        self.estimated_hours = estimated_hours
        self.completed = False

    # =====================================================
    # MARK TASK AS COMPLETED
    # =====================================================

    def mark_completed(self):
        self.completed = True

    # =====================================================
    # CALCULATE DAYS UNTIL DEADLINE
    # =====================================================

    def days_until_deadline(self, today):
        return (self.deadline - today).days

    # =====================================================
    # GET TASK STATUS
    # =====================================================

    def get_status(self):

        if self.completed:
            return "Completed"

        return "Pending"