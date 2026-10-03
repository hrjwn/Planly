from typing import List, Dict, Any
from datetime import date
from models.task import Task


class WorkloadAnalyzer:

    LOW_WORKLOAD_MAX = 3
    MEDIUM_WORKLOAD_MAX = 7

    @staticmethod
    def analyze(tasks: List[Task]) -> Dict[str, Any]:
        total = len(tasks)
        completed = sum(1 for t in tasks if t.is_completed())
        pending = total - completed

        if total > 0:
            completion_percentage = round((completed / total) * 100, 1)
        else:
            completion_percentage = 0.0

        if pending <= WorkloadAnalyzer.LOW_WORKLOAD_MAX:
            workload_level = "Low"
        elif pending <= WorkloadAnalyzer.MEDIUM_WORKLOAD_MAX:
            workload_level = "Medium"
        else:
            workload_level = "High"

        pending_list = [t for t in tasks if not t.is_completed()]

        upcoming_tasks = sorted(pending_list, key=lambda t: t.deadline_date() or date.max)
        overdue_tasks = [t for t in pending_list if t.is_overdue()]

        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for t in pending_list:
            if t.priority in priority_counts:
                priority_counts[t.priority] += 1
            else:
                priority_counts["Medium"] += 1

        subject_counts: Dict[str, int] = {}
        for t in tasks:
            subj = t.subject if t.subject else "General"
            subject_counts[subj] = subject_counts.get(subj, 0) + 1

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_percentage": completion_percentage,
            "workload_level": workload_level,
            "upcoming_tasks": upcoming_tasks,
            "overdue_tasks": overdue_tasks,
            "high_priority_pending": priority_counts["High"],
            "tasks_by_priority": priority_counts,
            "tasks_by_subject": subject_counts,
        }