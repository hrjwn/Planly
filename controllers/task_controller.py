from typing import List, Tuple
from datetime import date, datetime
from database.supabase_client import get_supabase_client
from models.task import Task

class TaskController:

    @staticmethod
    def get_student_tasks(student_id: str) -> List[Task]:
        if not student_id:
            return []

        client = get_supabase_client()
        try:
            response = (
                client.table("tasks")
                .select("*")
                .eq("student_id", student_id)
                .order("deadline", desc=False)
                .execute()
            )
            records = response.data or []
            return [Task.from_dict(row) for row in records]
        except Exception:
            return []

    @staticmethod
    def create_task(
        student_id: str, title: str, subject: str, deadline, priority: str
    ) -> Tuple[bool, str]:
        if not title or not title.strip():
            return False, "Please enter a task title."
        if not subject or not subject.strip():
            return False, "Please enter a subject/course."
        if not deadline:
            return False, "Please select a task deadline."

        new_task = Task(
            task_id=None,
            student_id=student_id,
            title=title,
            subject=subject,
            deadline=deadline,
            priority=priority,
            completed=False,
        )

        client = get_supabase_client()
        try:
            payload = new_task.to_dict()
            response = client.table("tasks").insert(payload).execute()
            if response.data:
                return True, f"Task '{new_task.title}' added successfully!"
            return False, "Could not save task. Please try again."
        except Exception as e:
            return False, f"Database error creating task: {str(e)}"

    @staticmethod
    def toggle_task_completion(task: Task) -> Tuple[bool, str]:
        if not task.task_id:
            return False, "Invalid task ID."

        new_status = not task.completed
        client = get_supabase_client()
        try:
            response = (
                client.table("tasks")
                .update({"completed": new_status})
                .eq("id", task.task_id)
                .execute()
            )
            if response.data:
                if new_status:
                    task.mark_completed()
                    return True, f"Marked '{task.title}' as completed."
                else:
                    task.mark_pending()
                    return True, f"Reopened '{task.title}' as pending."
            return False, "Could not update task status."
        except Exception as e:
            return False, f"Database error updating task: {str(e)}"

    @staticmethod
    def update_task(
        task_id: str,
        title: str,
        subject: str,
        deadline,
        priority: str,
        completed: bool = None,
    ) -> Tuple[bool, str]:
        if not task_id:
            return False, "Invalid task ID."
        if not title or not title.strip():
            return False, "Please enter a task title."
        if not subject or not subject.strip():
            return False, "Please enter a subject/course."
        if not deadline:
            return False, "Please select a task deadline."

        if isinstance(deadline, (datetime, date)):
            deadline_str = deadline.strftime("%Y-%m-%d")
        else:
            deadline_str = str(deadline).strip()

        clean_priority = priority.strip().capitalize() if priority else "Medium"
        if clean_priority not in ["Low", "Medium", "High"]:
            clean_priority = "Medium"

        update_payload = {
            "title": title.strip(),
            "subject": subject.strip(),
            "deadline": deadline_str,
            "priority": clean_priority,
        }
        if completed is not None:
            update_payload["completed"] = bool(completed)

        client = get_supabase_client()
        try:
            response = (
                client.table("tasks")
                .update(update_payload)
                .eq("id", task_id)
                .execute()
            )
            if response.data:
                return True, f"Task '{title.strip()}' updated successfully."
            return False, "Could not update task. Please try again."
        except Exception as e:
            return False, f"Database error updating task: {str(e)}"

    @staticmethod
    def delete_task(task_id: str) -> Tuple[bool, str]:
        if not task_id:
            return False, "Invalid task ID."

        client = get_supabase_client()
        try:
            response = client.table("tasks").delete().eq("id", task_id).execute()
            if response.data:
                return True, "Task deleted successfully."
            return False, "Failed to delete task or task not found."
        except Exception as e:
            return False, f"Database error deleting task: {str(e)}"