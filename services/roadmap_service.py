from typing import Dict, List, Any, Optional
from datetime import date, datetime
from models.task import Task
from models.subtask import Subtask

class RoadmapService:

    @staticmethod
    def task_progress(task: Task, subtasks: Optional[List[Subtask]]) -> float:
        """Fraction (0-1) of a main task that is done, based on its steps."""
        if task.is_completed():
            return 1.0
        if not subtasks:
            return 0.0
        done = sum(1 for s in subtasks if s.completed)
        return done / len(subtasks)

    @staticmethod
    def build_roadmap(
        tasks: List[Task], subtasks_by_task: Dict[str, List[Subtask]]
    ) -> List[Dict[str, Any]]:
        """One roadmap entry per main task: pending first (by deadline), then completed."""

        def sort_key(task: Task):
            try:
                due = datetime.strptime(task.deadline, "%Y-%m-%d").date()
            except Exception:
                due = date.max
            return (task.is_completed(), due, task.title)

        roadmap = []
        for task in sorted(tasks, key=sort_key):
            steps = subtasks_by_task.get(task.task_id, [])
            done = sum(1 for s in steps if s.completed)
            current_index = next(
                (i for i, s in enumerate(steps) if not s.completed), None
            )
            roadmap.append({
                "task": task,
                "steps": steps,
                "done_steps": done,
                "total_steps": len(steps),
                "current_index": None if task.is_completed() else current_index,
                "percentage": round(RoadmapService.task_progress(task, steps) * 100),
            })
        return roadmap
