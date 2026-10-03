from typing import Dict, List, Tuple
from database.supabase_client import get_supabase_client
from models.subtask import Subtask

class SubtaskController:

    @staticmethod
    def get_student_subtasks(student_id: str) -> Dict[str, List[Subtask]]:
        """Return every subtask for the student, grouped by parent task id."""
        if not student_id:
            return {}

        client = get_supabase_client()
        try:
            response = (
                client.table("subtasks")
                .select("*")
                .eq("student_id", student_id)
                .order("position", desc=False)
                .order("created_at", desc=False)
                .execute()
            )
            grouped: Dict[str, List[Subtask]] = {}
            for row in response.data or []:
                subtask = Subtask.from_dict(row)
                grouped.setdefault(subtask.task_id, []).append(subtask)
            return grouped
        except Exception:
            return {}

    @staticmethod
    def get_task_subtasks(task_id: str) -> List[Subtask]:
        if not task_id:
            return []

        client = get_supabase_client()
        try:
            response = (
                client.table("subtasks")
                .select("*")
                .eq("task_id", task_id)
                .order("position", desc=False)
                .order("created_at", desc=False)
                .execute()
            )
            return [Subtask.from_dict(row) for row in response.data or []]
        except Exception:
            return []

    @staticmethod
    def create_subtask(
        student_id: str, task_id: str, title: str, position: int = 0
    ) -> Tuple[bool, str]:
        if not task_id:
            return False, "Invalid task ID."
        if not title or not title.strip():
            return False, "Please enter a step title."

        new_subtask = Subtask(
            subtask_id=None,
            task_id=task_id,
            student_id=student_id,
            title=title,
            completed=False,
            position=position,
        )

        client = get_supabase_client()
        try:
            response = client.table("subtasks").insert(new_subtask.to_dict()).execute()
            if response.data:
                SubtaskController._sync_parent_task(task_id)
                return True, f"Step '{new_subtask.title}' added."
            return False, "Could not save step. Please try again."
        except Exception as e:
            return False, f"Database error creating step: {str(e)}"

    @staticmethod
    def set_subtask_completion(subtask: Subtask, completed: bool) -> Tuple[bool, str]:
        if not subtask.subtask_id:
            return False, "Invalid step ID."

        client = get_supabase_client()
        try:
            response = (
                client.table("subtasks")
                .update({"completed": bool(completed)})
                .eq("id", subtask.subtask_id)
                .execute()
            )
            if response.data:
                subtask.completed = bool(completed)
                SubtaskController._sync_parent_task(subtask.task_id)
                return True, "Step updated."
            return False, "Could not update step."
        except Exception as e:
            return False, f"Database error updating step: {str(e)}"

    @staticmethod
    def delete_subtask(subtask: Subtask) -> Tuple[bool, str]:
        if not subtask.subtask_id:
            return False, "Invalid step ID."

        client = get_supabase_client()
        try:
            response = client.table("subtasks").delete().eq("id", subtask.subtask_id).execute()
            if response.data:
                SubtaskController._sync_parent_task(subtask.task_id)
                return True, "Step deleted."
            return False, "Failed to delete step or step not found."
        except Exception as e:
            return False, f"Database error deleting step: {str(e)}"

    @staticmethod
    def _sync_parent_task(task_id: str):
        """A main task is complete exactly when all of its steps are complete."""
        client = get_supabase_client()
        try:
            response = (
                client.table("subtasks")
                .select("completed")
                .eq("task_id", task_id)
                .execute()
            )
            rows = response.data or []
            if not rows:
                return
            all_done = all(row.get("completed") for row in rows)
            client.table("tasks").update({"completed": all_done}).eq("id", task_id).execute()
        except Exception:
            pass
