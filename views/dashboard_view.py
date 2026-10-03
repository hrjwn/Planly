import streamlit as st
import pandas as pd
from models.student import Student
from controllers.task_controllers import TaskController
from services.workload_analyzer import WorkloadAnalyzer
from services.recommendation_service import RecommendationService


def render_dashboard(student: Student):
    tasks = TaskController.get_student_tasks(student.student_id)

    analysis = WorkloadAnalyzer.analyze(tasks)
    workload_level = analysis["workload_level"]
    primary_rec = RecommendationService.get_primary_recommendation(workload_level)

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.06em;">TOTAL TASKS</div>
                <div style="font-size: 2.1rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{analysis['total_tasks']}</div>
                <div style="font-size: 0.8rem; color: #8A737D;">All tracked assignments</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.06em;">COMPLETED</div>
                <div style="font-size: 2.1rem; font-weight: 700; color: #C95A8D; margin: 0.2rem 0;">{analysis['completed_tasks']}</div>
                <div style="font-size: 0.8rem; color: #8A737D;">Finished deliverables</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.06em;">PENDING</div>
                <div style="font-size: 2.1rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{analysis['pending_tasks']}</div>
                <div style="font-size: 0.8rem; color: #8A737D;">Awaiting completion</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        workload_bg = "#FFF0F5" if workload_level == "Low" else ("#FDF2F7" if workload_level == "Medium" else "#FCE4EC")
        workload_color = "#3B3036"
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.06em;">WORKLOAD</div>
                <div style="font-size: 2.1rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{workload_level}</div>
                <div style="font-size: 0.8rem; color: #8A737D;">Based on pending items</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-top: 0.5rem; margin-bottom: 0.5rem;">
            Quick Actions
        </div>
        """,
        unsafe_allow_html=True,
    )

    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)

    with qa_col1:
        if st.button("Add New Task", key="qa_add_task", use_container_width=True, type="primary"):
            st.session_state.page_to_navigate = "My Tasks"
            st.session_state.open_add_task = True
            st.rerun()

    with qa_col2:
        if st.button("View Tasks", key="qa_view_tasks", use_container_width=True):
            st.session_state.page_to_navigate = "My Tasks"
            st.rerun()

    with qa_col3:
        if st.button("Check Progress", key="qa_check_progress", use_container_width=True):
            st.session_state.page_to_navigate = "My Progress"
            st.rerun()

    with qa_col4:
        if st.button("Edit Profile", key="qa_edit_profile", use_container_width=True):
            st.session_state.page_to_navigate = "Profile"
            st.rerun()

    st.write("")

    pct = analysis["completion_percentage"]
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.3rem;">
            <span style="font-size: 0.95rem; font-weight: 600; color: #3B3036;">Overall Academic Progress</span>
            <span style="font-size: 0.95rem; font-weight: 700; color: #D96C9D;">{pct}% Completed</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(pct / 100.0)

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.7rem;">
                Upcoming Deadlines
            </div>
            """,
            unsafe_allow_html=True,
        )
        upcoming = analysis["upcoming_tasks"]

        if not upcoming:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                    No upcoming deadlines. All active tasks are completed!
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for task in upcoming[:5]:
                days_left = task.days_until_deadline()

                if days_left < 0:
                    urgency_badge = f"<span style='background-color: #FEE2E2; color: #B91C1C; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Overdue by {abs(days_left)}d</span>"
                elif days_left == 0:
                    urgency_badge = "<span style='background-color: #FEF3C7; color: #B45309; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Due Today</span>"
                elif days_left == 1:
                    urgency_badge = "<span style='background-color: #FEF3C7; color: #B45309; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Due Tomorrow</span>"
                else:
                    urgency_badge = f"<span style='background-color: #FCE8F0; color: #C95A8D; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Due in {days_left}d</span>"

                p_badge_colors = {
                    "High": "background-color: #FDF2F8; color: #BE185D; border: 1px solid #FBCFE8;",
                    "Medium": "background-color: #FFF7ED; color: #C2410C; border: 1px solid #FFEDD5;",
                    "Low": "background-color: #F0FDF4; color: #15803D; border: 1px solid #DCFCE7;",
                }
                priority_style = p_badge_colors.get(task.priority, "background-color: #F3F4F6; color: #4B5563;")

                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                            <div style="font-weight: 600; color: #3B3036; font-size: 0.95rem;">{task.title}</div>
                            {urgency_badge}
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #8A737D;">
                            <span>Subject: <b>{task.subject}</b></span>
                            <span>•</span>
                            <span>Date: {task.deadline}</span>
                            <span>•</span>
                            <span style="{priority_style} padding: 1px 7px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">{task.priority} Priority</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col_right:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.7rem;">
                Active Task Overview
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not tasks:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                    No tasks found. Use Quick Actions above to add your first academic task.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            data_rows = [
                {
                    "Task": t.title,
                    "Subject": t.subject,
                    "Deadline": t.deadline,
                    "Priority": t.priority,
                    "Status": "Completed" if t.completed else "Pending",
                }
                for t in tasks
            ]
            df = pd.DataFrame(data_rows)
            st.dataframe(df, use_container_width=True, hide_index=True)