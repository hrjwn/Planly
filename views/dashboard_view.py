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
    pct = analysis["completion_percentage"]

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
                Course/Grade Level: <span style="color: #D96C9D; font-weight: 600;">{student.course}</span> | Status: <span style="color: #3B3036; font-weight: 600;">{workload_level} Workload</span>
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
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.06em;">WORKLOAD LEVEL</div>
                <div style="font-size: 2.1rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{workload_level}</div>
                <div style="font-size: 0.8rem; color: #8A737D;">Based on active tasks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-top: 0.2rem; margin-bottom: 0.5rem;">
            Quick Actions
        </div>
        """,
        unsafe_allow_html=True,
    )

    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)

    with qa_col1:
        if st.button("Add Task", key="qa_add_task", use_container_width=True, type="primary"):
            st.session_state.page_to_navigate = "My Tasks"
            st.session_state.open_add_task = True
            st.rerun()

    with qa_col2:
        if st.button("Start Focus Session", key="qa_start_focus", use_container_width=True):
            st.session_state.page_to_navigate = "Focus"
            st.rerun()

    with qa_col3:
        if st.button("View My Tasks", key="qa_view_tasks", use_container_width=True):
            st.session_state.page_to_navigate = "My Tasks"
            st.rerun()

    with qa_col4:
        if st.button("View My Progress", key="qa_view_progress", use_container_width=True):
            st.session_state.page_to_navigate = "My Progress"
            st.rerun()

    st.write("")

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
                    Workload Analysis: {workload_level} Load
                </span>
                <span style="font-size: 0.9rem; color: #3B3036;">
                    {primary_rec}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 700; color: #3B3036; margin-bottom: 0.6rem;">
            Today's Plan
        </div>
        """,
        unsafe_allow_html=True,
    )

    todays_plan_tasks = analysis["todays_plan"]

    if not todays_plan_tasks:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.6rem; text-align: center; color: #8A737D; font-size: 0.92rem; margin-bottom: 1.5rem;">
                No active tasks require attention today. You are completely caught up!
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for plan_task in todays_plan_tasks[:4]:
            days_left = plan_task.days_until_deadline()
            deadline_label = plan_task.get_deadline_label()

            if days_left < 0:
                badge_style = "background-color: #FEE2E2; color: #B91C1C; border: 1px solid #FECACA;"
            elif days_left == 0:
                badge_style = "background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;"
            elif days_left == 1:
                badge_style = "background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;"
            else:
                badge_style = "background-color: #FCE8F0; color: #C95A8D; border: 1px solid #F3B6CF;"

            p_colors = {
                "High": "background-color: #FDF2F8; color: #BE185D; border: 1px solid #FBCFE8;",
                "Medium": "background-color: #FFF7ED; color: #C2410C; border: 1px solid #FFEDD5;",
                "Low": "background-color: #F0FDF4; color: #15803D; border: 1px solid #DCFCE7;",
            }
            priority_style = p_colors.get(plan_task.priority, "background-color: #F3F4F6; color: #4B5563;")

            plan_card_col, plan_action_col = st.columns([3.8, 1.2])

            with plan_card_col:
                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.5rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                            <div style="font-weight: 600; color: #3B3036; font-size: 0.95rem;">{plan_task.title}</div>
                            <span style="{badge_style} padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{deadline_label}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #8A737D;">
                            <span>Subject: <b>{plan_task.subject}</b></span>
                            <span>•</span>
                            <span>Deadline: {plan_task.deadline}</span>
                            <span>•</span>
                            <span style="{priority_style} padding: 1px 7px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">{plan_task.priority} Priority</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with plan_action_col:
                if st.button("Focus", key=f"plan_focus_{plan_task.task_id}", use_container_width=True):
                    st.session_state.focus_target_task_id = plan_task.task_id
                    st.session_state.page_to_navigate = "Focus"
                    st.rerun()

    st.write("")

    col_needs_attention, col_upcoming = st.columns([1, 1])

    with col_needs_attention:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.7rem;">
                Needs Attention
            </div>
            """,
            unsafe_allow_html=True,
        )

        needs_attention_tasks = analysis["needs_attention"]

        if not needs_attention_tasks:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.88rem;">
                    No urgent tasks. No overdue assignments or pressing deadlines detected.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for task in needs_attention_tasks[:4]:
                days_left = task.days_until_deadline()
                if days_left < 0:
                    badge_style = "background-color: #FEE2E2; color: #B91C1C;"
                    reason = f"Overdue by {abs(days_left)} days"
                elif days_left == 0:
                    badge_style = "background-color: #FEF3C7; color: #B45309;"
                    reason = "Due Today"
                elif days_left <= 2:
                    badge_style = "background-color: #FEF3C7; color: #B45309;"
                    reason = f"Due in {days_left} days"
                else:
                    badge_style = "background-color: #FDF2F8; color: #BE185D;"
                    reason = f"{task.priority} Priority"

                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.85rem 1.1rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                            <span style="font-weight: 600; color: #3B3036; font-size: 0.92rem;">{task.title}</span>
                            <span style="{badge_style} padding: 2px 7px; border-radius: 5px; font-size: 0.74rem; font-weight: 600;">{reason}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #8A737D;">
                            Subject: {task.subject} | Due: {task.deadline}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col_upcoming:
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
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.88rem;">
                    No pending deadlines. All active tasks are completed!
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for task in upcoming[:4]:
                label = task.get_deadline_label()
                days_left = task.days_until_deadline()

                if days_left < 0:
                    badge_style = "background-color: #FEE2E2; color: #B91C1C;"
                elif days_left <= 1:
                    badge_style = "background-color: #FEF3C7; color: #B45309;"
                else:
                    badge_style = "background-color: #FCE8F0; color: #C95A8D;"

                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.85rem 1.1rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                            <span style="font-weight: 600; color: #3B3036; font-size: 0.92rem;">{task.title}</span>
                            <span style="{badge_style} padding: 2px 7px; border-radius: 5px; font-size: 0.74rem; font-weight: 600;">{label}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #8A737D;">
                            Subject: {task.subject} | Due: {task.deadline} | Priority: {task.priority}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )