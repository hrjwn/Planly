from typing import List, Dict, Any
from models.task import Task

class StudyScheduler:

    @staticmethod
    def generate_task_schedule(task: Task) -> List[Dict[str, str]]:
        days = task.days_until_deadline()
        priority = task.priority

        if days < 0:
            return [
                {"day": "Immediate", "activity": "Finalize remaining requirements and submit overdue deliverable promptly."}
            ]
        elif days == 0:
            return [
                {"day": "Today", "activity": "Complete all pending sections, run final verification, and submit before deadline."}
            ]
        elif days == 1:
            return [
                {"day": "Today", "activity": "Draft core content, complete main calculations or implementation."},
                {"day": "Tomorrow", "activity": "Perform final proofreading, rubric review, and submit."}
            ]
        elif days == 2:
            return [
                {"day": "Today", "activity": "Research materials, create outline, and establish core setup."},
                {"day": "Tomorrow", "activity": "Execute core assignment tasks and write major components."},
                {"day": "Due Date", "activity": "Run testing, review formatting, and submit."}
            ]
        elif days == 3:
            return [
                {"day": "Today", "activity": "Review assignment instructions and conduct initial research."},
                {"day": "Tomorrow", "activity": "Implement central logic, analysis, or draft sections."},
                {"day": "Next Day", "activity": "Refine draft, test edge cases, and polish explanations."},
                {"day": "Due Date", "activity": "Final checks, export files, and submit."}
            ]
        else:
            if priority == "High":
                return [
                    {"day": "Today", "activity": "Analyze project scope, gather references, and set milestone goals."},
                    {"day": "Next 2 Days", "activity": "Schedule focused 45-minute study sessions for intensive development."},
                    {"day": "Day Before Due Date", "activity": "Comprehensive review, debugging, and proofreading."},
                    {"day": "Due Date", "activity": "Final submission and rubric verification."}
                ]
            else:
                return [
                    {"day": "This Week", "activity": "Examine instructions, set up workspace, and collect required notes."},
                    {"day": "Mid-point", "activity": "Work through main problem sets or drafted chapters."},
                    {"day": "Day Before Due Date", "activity": "Complete final edits and prepare submission package."}
                ]

    @staticmethod
    def get_general_recommendations(pending_tasks_count: int, high_priority_count: int, workload_level: str) -> List[str]:
        recommendations = []

        if workload_level == "High":
            recommendations.append(
                "High Workload Strategy: Break your study time into 25-minute Pomodoro sessions with 5-minute restorative breaks to sustain focus without burning out."
            )
            recommendations.append(
                "Triage Focus: Reserve your primary morning or early evening study block for high-priority and imminent deadlines first."
            )
        elif workload_level == "Medium":
            recommendations.append(
                "Balanced Schedule: Schedule 1 to 2 uninterrupted 45-minute focus blocks today to complete one deliverable and keep your queue manageable."
            )
            recommendations.append(
                "Pacing Plan: Spread the remaining assignments evenly across the next three days rather than clustering them on the due date."
            )
        else:
            recommendations.append(
                "Maintenance Routine: Your academic workload is well under control. Dedicate 25 minutes today for syllabus review or light preparation."
            )
            recommendations.append(
                "Proactive Learning: Review upcoming lecture topics in advance to stay ahead of the next assignment cycle."
            )

        if high_priority_count > 1:
            recommendations.append(
                f"Multiple Critical Tasks: You have {high_priority_count} high-priority tasks. Work on the one due earliest first to minimize deadline pressure."
            )

        recommendations.append(
            "Study Habit: Set a dedicated start time for each study session and remove distracting notifications during active focus blocks."
        )

        return recommendations

    @classmethod
    def create_schedule(cls, tasks: List[Task], workload_level: str) -> Dict[str, Any]:
        pending = [t for t in tasks if not t.is_completed()]
        high_priority = [t for t in pending if t.priority == "High"]

        task_schedules = []
        for task in pending:
            task_schedules.append({
                "task": task,
                "schedule": cls.generate_task_schedule(task)
            })

        general_tips = cls.get_general_recommendations(
            pending_tasks_count=len(pending),
            high_priority_count=len(high_priority),
            workload_level=workload_level
        )

        return {
            "task_schedules": task_schedules,
            "general_tips": general_tips
        }
