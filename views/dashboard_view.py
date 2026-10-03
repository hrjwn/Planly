import streamlit as st
import pandas as pd
from models.student import Student
from controllers.task_controller import TaskController
from services.workload_analyzer import WorkloadAnalyzer
from services.recommendation_service import RecommendationService
from ui.components import (
    html,
    section_title,
    stat_card,
    empty_state,
    priority_badge_style,
    deadline_badge,
)

QUICK_ACTIONS = [
    # (label, button key, target page, open the add-task form)
    ("Add New Task", "qa_add_task", "My Tasks", True),
    ("View Tasks", "qa_view_tasks", "My Tasks", False),
    ("Check Progress", "qa_check_progress", "My Progress", False),
    ("Edit Profile", "qa_edit_profile", "Profile", False),
]


def render_dashboard(student: Student):
    tasks = TaskController.get_student_tasks(student.student_id)

    analysis = WorkloadAnalyzer.analyze(tasks)
    workload_level = analysis["workload_level"]
    primary_rec = RecommendationService.get_primary_recommendation(workload_level)

    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-left: 6px solid #D96C9D; padding: 1.5rem 1.8rem; border-radius: 14px; margin-bottom: 1.5rem; box-shadow: 0 2px 10px rgba(217, 108, 157, 0.06);">
            <div style="font-size: 0.82rem; font-weight: 600; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem;">
                Academic Overview
            </div>
            <h2 style="margin: 0; color: #3B3036; font-size: 1.8rem; font-weight: 700;">
                Welcome back, {student.name}
            </h2>
            <p style="margin: 0.4rem 0 0 0; color: #8A737D; font-size: 0.95rem;">
                Here's an overview of your academic workload. | Course: <span style="color: #D96C9D; font-weight: 600;">{student.course}</span>
            </p>
        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total Tasks", analysis["total_tasks"], "All tracked assignments", large=True)
    with c2:
        stat_card("Completed", analysis["completed_tasks"], "Finished deliverables", "#C95A8D", large=True)
    with c3:
        stat_card("Pending", analysis["pending_tasks"], "Awaiting completion", "#D96C9D", large=True)
    with c4:
        stat_card("Workload", workload_level, "Based on pending items", "#D96C9D", large=True)

    st.write("")

    section_title("Quick Actions", margin="0.5rem 0 0.5rem 0")

    for col, (label, key, target, open_add) in zip(st.columns(4), QUICK_ACTIONS):
        with col:
            button_type = "primary" if open_add else "secondary"
            if st.button(label, key=key, use_container_width=True, type=button_type):
                st.session_state.page_to_navigate = target
                if open_add:
                    st.session_state.open_add_task = True
                st.rerun()

    st.write("")

    pct = analysis["completion_percentage"]
    html(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.3rem;">
            <span style="font-size: 0.95rem; font-weight: 600; color: #3B3036;">Overall Academic Progress</span>
            <span style="font-size: 0.95rem; font-weight: 700; color: #D96C9D;">{pct}% Completed</span>
        </div>
        """
    )
    st.progress(pct / 100.0)

    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem 1.4rem; margin-top: 1rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-size: 0.75rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 0.2rem;">
                    Workload Status: {workload_level} Load
                </span>
                <span style="font-size: 0.9rem; color: #3B3036;">
                    {primary_rec}
                </span>
            </div>
        </div>
        """
    )

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        section_title("Upcoming Deadlines")
        upcoming = analysis["upcoming_tasks"]

        if not upcoming:
            empty_state("No upcoming deadlines. All active tasks are completed!")
        else:
            for task in upcoming[:5]:
                badge_text, badge_style = deadline_badge(task.days_until_deadline())
                html(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                            <div style="font-weight: 600; color: #3B3036; font-size: 0.95rem;">{task.title}</div>
                            <span style="{badge_style} padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{badge_text}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #8A737D;">
                            <span>Subject: <b>{task.subject}</b></span>
                            <span>•</span>
                            <span>Date: {task.deadline}</span>
                            <span>•</span>
                            <span style="{priority_badge_style(task.priority)} padding: 1px 7px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">{task.priority} Priority</span>
                        </div>
                    </div>
                    """
                )

    with col_right:
        section_title("Active Task Overview")

        if not tasks:
            empty_state("No tasks found. Use Quick Actions above to add your first academic task.")
        else:
            df = pd.DataFrame(
                {
                    "Task": t.title,
                    "Subject": t.subject,
                    "Deadline": t.deadline,
                    "Priority": t.priority,
                    "Status": "Completed" if t.completed else "Pending",
                }
                for t in tasks
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
