# =========================================================
# WORKLOAD ANALYZER SERVICE
# Planly - Student Workload & Task Management System
# =========================================================

from datetime import date


class WorkloadAnalyzer:
    """
    Calculates and evaluates a student's workload.
    """

    # =====================================================
    # CALCULATE WORKLOAD SCORE
    # =====================================================

    def calculate_score(self, student):

        pending_tasks = student.get_pending_tasks()

        if not pending_tasks:
            return 0

        score = 0

        for task in pending_tasks:

            # ---------------------------------------------
            # PRIORITY POINTS
            # ---------------------------------------------

            if task.priority == "High":
                score += 3

            elif task.priority == "Medium":
                score += 2

            else:
                score += 1

            # ---------------------------------------------
            # DEADLINE POINTS
            # ---------------------------------------------

            days_left = task.days_until_deadline(
                date.today()
            )

            if days_left <= 1:
                score += 3

            elif days_left <= 3:
                score += 2

            elif days_left <= 7:
                score += 1

            # ---------------------------------------------
            # STUDY TIME POINTS
            # ---------------------------------------------

            if task.estimated_hours >= 4:
                score += 2

            elif task.estimated_hours >= 2:
                score += 1

        return score

    # =====================================================
    # GET WORKLOAD LEVEL
    # =====================================================

    def get_workload_level(self, score):

        if score <= 5:
            return "LOW"

        elif score <= 10:
            return "MODERATE"

        else:
            return "HIGH"

    # =====================================================
    # GET WORKLOAD MESSAGE
    # =====================================================

    def get_workload_message(self, level):

        if level == "LOW":

            return (
                "Your workload is manageable. "
                "Keep up your study routine."
            )

        elif level == "MODERATE":

            return (
                "Your workload is starting to increase. "
                "Try planning your study time early."
            )

        else:

            return (
                "Your workload is HIGH. "
                "Consider moving your lowest-priority "
                "task to next week."
            )