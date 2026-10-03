from typing import List, Dict, Any, Optional
from datetime import date, datetime
from models.task import Task
from models.subtask import Subtask
from services.roadmap_service import RoadmapService

class WorkloadAnalyzer:

    LOW_WORKLOAD_MAX = 3
    MEDIUM_WORKLOAD_MAX = 7

    @staticmethod
    def analyze(
        tasks: List[Task],
        subtasks_by_task: Optional[Dict[str, List[Subtask]]] = None,
    ) -> Dict[str, Any]:
        subtasks_by_task = subtasks_by_task or {}
        total = len(tasks)
        completed = sum(1 for t in tasks if t.is_completed())
        pending = total - completed

        # Completed steps give partial credit toward their main task.
        progress_by_id = {
            t.task_id: RoadmapService.task_progress(t, subtasks_by_task.get(t.task_id))
            for t in tasks
        }

        if total > 0:
            completion_percentage = round((sum(progress_by_id.values()) / total) * 100, 1)
        else:
            completion_percentage = 0.0

        if pending <= WorkloadAnalyzer.LOW_WORKLOAD_MAX:
            workload_level = "Low"
        elif pending <= WorkloadAnalyzer.MEDIUM_WORKLOAD_MAX:
            workload_level = "Medium"
        else:
            workload_level = "High"

        pending_tasks = [t for t in tasks if not t.is_completed()]

        def parse_deadline(task: Task):
            try:
                return datetime.strptime(task.deadline, "%Y-%m-%d").date()
            except Exception:
                return date.max

        upcoming_tasks = sorted(pending_tasks, key=parse_deadline)
        overdue_tasks = [t for t in pending_tasks if t.is_overdue()]
        due_today_tasks = [t for t in pending_tasks if t.days_until_deadline() == 0]
        due_soon_tasks = [t for t in pending_tasks if 0 < t.days_until_deadline() <= 2]

        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for t in pending_tasks:
            if t.priority in priority_counts:
                priority_counts[t.priority] += 1
            else:
                priority_counts["Medium"] += 1

        subject_counts: Dict[str, int] = {}
        subject_progress: Dict[str, Dict[str, Any]] = {}
        for t in tasks:
            subj = t.subject if t.subject else "General"
            subject_counts[subj] = subject_counts.get(subj, 0) + 1
            if subj not in subject_progress:
                subject_progress[subj] = {"total": 0, "completed": 0, "pending": 0, "percentage": 0.0, "progress_sum": 0.0}
            subject_progress[subj]["total"] += 1
            subject_progress[subj]["progress_sum"] += progress_by_id[t.task_id]
            if t.is_completed():
                subject_progress[subj]["completed"] += 1
            else:
                subject_progress[subj]["pending"] += 1

        for subj, stats in subject_progress.items():
            if stats["total"] > 0:
                stats["percentage"] = round((stats.pop("progress_sum") / stats["total"]) * 100, 1)

        todays_plan_ids = set()
        todays_plan: List[Task] = []

        for task in overdue_tasks:
            if task.task_id not in todays_plan_ids:
                todays_plan.append(task)
                todays_plan_ids.add(task.task_id)

        for task in due_today_tasks:
            if task.task_id not in todays_plan_ids:
                todays_plan.append(task)
                todays_plan_ids.add(task.task_id)

        high_priority_upcoming = [t for t in upcoming_tasks if t.priority == "High" and t.task_id not in todays_plan_ids]
        for task in high_priority_upcoming:
            todays_plan.append(task)
            todays_plan_ids.add(task.task_id)

        other_upcoming = [t for t in upcoming_tasks if t.task_id not in todays_plan_ids]
        for task in other_upcoming:
            todays_plan.append(task)
            todays_plan_ids.add(task.task_id)

        needs_attention_ids = set()
        needs_attention: List[Task] = []

        for task in overdue_tasks:
            if task.task_id not in needs_attention_ids:
                needs_attention.append(task)
                needs_attention_ids.add(task.task_id)

        for task in due_today_tasks:
            if task.task_id not in needs_attention_ids:
                needs_attention.append(task)
                needs_attention_ids.add(task.task_id)

        for task in due_soon_tasks:
            if task.task_id not in needs_attention_ids:
                needs_attention.append(task)
                needs_attention_ids.add(task.task_id)

        for task in pending_tasks:
            if task.priority == "High" and task.task_id not in needs_attention_ids:
                needs_attention.append(task)
                needs_attention_ids.add(task.task_id)

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_percentage": completion_percentage,
            "workload_level": workload_level,
            "upcoming_tasks": upcoming_tasks,
            "overdue_tasks": overdue_tasks,
            "due_today_tasks": due_today_tasks,
            "due_soon_tasks": due_soon_tasks,
            "high_priority_pending": priority_counts["High"],
            "tasks_by_priority": priority_counts,
            "tasks_by_subject": subject_counts,
            "subject_progress": subject_progress,
            "todays_plan": todays_plan,
            "needs_attention": needs_attention,
        }