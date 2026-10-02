# =========================================================
# STUDY SCHEDULER SERVICE
# Planly - Student Workload & Task Management System
# =========================================================

from datetime import date


class StudyScheduler:
    """
    Generates study schedule recommendations
    based on deadlines and estimated study time.
    """

    # =====================================================
    # GENERATE STUDY SCHEDULE
    # =====================================================

    def generate_schedule(self, student):

        pending_tasks = student.get_pending_tasks()

        if not pending_tasks:
            return []

        # ---------------------------------------------
        # SORT TASKS BY DEADLINE
        # ---------------------------------------------

        pending_tasks = sorted(
            pending_tasks,
            key=lambda task: task.deadline
        )

        schedule = []

        # ---------------------------------------------
        # CREATE RECOMMENDATION FOR EACH TASK
        # ---------------------------------------------

        for task in pending_tasks:

            days_left = task.days_until_deadline(
                date.today()
            )

            # -----------------------------------------
            # DETERMINE NUMBER OF STUDY DAYS
            # -----------------------------------------

            if days_left <= 0:

                study_days = 1

            elif days_left == 1:

                study_days = 1

            elif days_left <= 3:

                study_days = 2

            else:

                study_days = min(
                    days_left,
                    3
                )

            # -----------------------------------------
            # CALCULATE DAILY STUDY HOURS
            # -----------------------------------------

            daily_hours = (
                task.estimated_hours
                / study_days
            )

            # -----------------------------------------
            # SAVE RECOMMENDATION
            # -----------------------------------------

            schedule.append(
                {
                    "task": task,
                    "study_days": study_days,
                    "daily_hours": daily_hours
                }
            )

        return schedule