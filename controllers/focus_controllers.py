from typing import List, Tuple, Dict, Any
from datetime import date, datetime, timedelta
import streamlit as st
from database.supabase_client import get_supabase_client
from models.focus_session import FocusSession

class FocusController:

    @staticmethod
    def format_duration(total_minutes: int) -> str:
        if not total_minutes or total_minutes <= 0:
            return "0m"
        hours = total_minutes // 60
        mins = total_minutes % 60
        if hours > 0 and mins > 0:
            return f"{hours}h {mins}m"
        elif hours > 0:
            return f"{hours}h"
        return f"{mins}m"

    @staticmethod
    def record_focus_session(
        student_id: str,
        task_id: str,
        duration: int,
        subject: str = "",
        task_title: str = "",
        completed: bool = True,
    ) -> Tuple[bool, str]:
        if not student_id:
            return False, "Invalid student ID."

        session_date_str = date.today().strftime("%Y-%m-%d")

        payload = {
            "student_id": student_id,
            "task_id": task_id if task_id else None,
            "duration": int(duration),
            "session_date": session_date_str,
            "completed": bool(completed),
            "subject": subject.strip() if subject else "General Study",
        }

        local_session = FocusSession(
            session_id=None,
            student_id=student_id,
            task_id=task_id,
            duration=duration,
            session_date=session_date_str,
            completed=completed,
            subject=subject or "General Study",
            task_title=task_title,
        )

        if "cached_focus_sessions" not in st.session_state:
            st.session_state.cached_focus_sessions = []
        st.session_state.cached_focus_sessions.append(local_session)

        client = get_supabase_client()
        try:
            client.table("focus_sessions").insert(payload).execute()
            return True, "Focus session recorded successfully."
        except Exception:
            return True, "Focus session recorded locally for this session."

    @staticmethod
    def get_student_focus_sessions(student_id: str) -> List[FocusSession]:
        if not student_id:
            return []

        client = get_supabase_client()
        db_sessions = []

        try:
            response = (
                client.table("focus_sessions")
                .select("*")
                .eq("student_id", student_id)
                .order("session_date", desc=True)
                .execute()
            )
            records = response.data or []
            for row in records:
                db_sessions.append(FocusSession.from_dict(row))
        except Exception:
            pass

        cached = st.session_state.get("cached_focus_sessions", [])
        student_cached = [s for s in cached if s.student_id == student_id]

        if not db_sessions:
            return student_cached

        db_ids = {s.session_id for s in db_sessions if s.session_id}
        combined = list(db_sessions)
        for s in student_cached:
            if s.session_id and s.session_id not in db_ids:
                combined.append(s)

        return combined

    @classmethod
    def get_weekly_focus_summary(cls, student_id: str) -> Dict[str, Any]:
        sessions = cls.get_student_focus_sessions(student_id)

        today = date.today()
        seven_days_ago = today - timedelta(days=7)

        total_sessions = len(sessions)
        total_minutes = sum(s.duration for s in sessions if s.completed)

        weekly_sessions_list = []
        for s in sessions:
            try:
                s_date = datetime.strptime(s.session_date, "%Y-%m-%d").date()
                if seven_days_ago <= s_date <= today and s.completed:
                    weekly_sessions_list.append(s)
            except Exception:
                if s.completed:
                    weekly_sessions_list.append(s)

        weekly_sessions_count = len(weekly_sessions_list)
        weekly_minutes = sum(s.duration for s in weekly_sessions_list)

        return {
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
            "formatted_total_time": cls.format_duration(total_minutes),
            "weekly_sessions": weekly_sessions_count,
            "weekly_minutes": weekly_minutes,
            "formatted_weekly_time": cls.format_duration(weekly_minutes),
            "all_sessions": sessions,
        }
