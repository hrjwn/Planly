from datetime import date, timedelta
import streamlit as st
import pandas as pd
from models.student import Student
from controllers.task_controller import TaskController
from services.workload_analyzer import WorkloadAnalyzer
from services.recommendation_service import RecommendationService
from ui.components import html, page_header, section_title, stat_card, empty_state, deadline_badge


def render_progress_view(student: Student):
    tasks = TaskController.get_student_tasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks)
    workload = analysis["workload_level"]
    pct = analysis["completion_percentage"]
    total = analysis["total_tasks"]
    completed = analysis["completed_tasks"]
    pending = analysis["pending_tasks"]
    upcoming = analysis["upcoming_tasks"]

    today = date.today()
    one_week_later = today + timedelta(days=7)
    deadlines_this_week = sum(
        1 for t in upcoming
        if t.deadline_date() and today <= t.deadline_date() <= one_week_later
    )

    page_header(
        "My Progress",
        "Track your semester momentum, workload balance, and academic task completion.",
    )

    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 14px rgba(217, 108, 157, 0.06);">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.8rem;">
                <div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem;">
                        YOUR PROGRESS
                    </div>
                    <div style="font-size: 2.8rem; font-weight: 800; color: #3B3036; line-height: 1;">
                        {pct}%
                    </div>
                    <div style="font-size: 0.95rem; color: #8A737D; margin-top: 0.3rem;">
                        {completed} of {total} tasks completed
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem;">
                        CURRENT WORKLOAD
                    </div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #D96C9D;">
                        {workload}
                    </div>
                    <div style="font-size: 0.85rem; color: #8A737D; margin-top: 0.3rem;">
                        UPCOMING: {deadlines_this_week} deadline(s) this week
                    </div>
                </div>
            </div>
        </div>
        """
    )

    st.progress(pct / 100.0 if total > 0 else 0.0)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total Tasks", total, "Semester assignments")
    with c2:
        stat_card("Completed Tasks", completed, "Submitted work", "#C95A8D")
    with c3:
        stat_card("Pending Tasks", pending, "Active workload", "#D96C9D")
    with c4:
        stat_card("Completion Rate", f"{pct}%", "Overall completion")

    st.write("")

    section_title("Study Suggestions", size="1.15rem", margin="1rem 0 0.6rem 0")

    primary_advice = RecommendationService.get_primary_recommendation(workload)
    detailed_tips = RecommendationService.get_detailed_recommendations(analysis)

    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-left: 6px solid #D96C9D; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05);">
            <div style="font-size: 0.8rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.3rem;">
                Workload Strategy: {workload} Workload
            </div>
            <div style="font-size: 0.98rem; font-weight: 600; color: #3B3036; margin-bottom: 0.6rem;">
                {primary_advice}
            </div>
            <div style="border-top: 1px solid #FCE8F0; padding-top: 0.6rem;">
                <ul style="margin: 0; padding-left: 1.2rem; color: #8A737D; font-size: 0.88rem; line-height: 1.6;">
                    {''.join(f'<li style="margin-bottom: 0.3rem;"><span style="color: #3B3036;">{tip}</span></li>' for tip in detailed_tips)}
                </ul>
            </div>
        </div>
        """
    )

    col_timeline, col_charts = st.columns([1.1, 0.9])

    with col_timeline:
        section_title("Timeline: Upcoming Deadlines")

        if not upcoming:
            empty_state("No pending deadlines. Excellent job managing your assignments!")
        else:
            for task in upcoming:
                badge_str, badge_style = deadline_badge(task.days_until_deadline(), long_units=True)

                html(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                            <div style="font-weight: 600; color: #3B3036; font-size: 0.92rem;">{task.title}</div>
                            <span style="{badge_style} padding: 2px 7px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">{badge_str}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #8A737D;">
                            Subject: {task.subject} | Priority: <b>{task.priority}</b> | Date: {task.deadline}
                        </div>
                    </div>
                    """
                )

    with col_charts:
        section_title("Task Breakdown")

        p_counts = analysis["tasks_by_priority"]
        df_priority = pd.DataFrame({
            "Priority": list(p_counts.keys()),
            "Pending Tasks": list(p_counts.values()),
        })
        st.caption("Pending Tasks by Priority Level")
        st.bar_chart(df_priority.set_index("Priority"), height=180)

        s_counts = analysis["tasks_by_subject"]
        if s_counts:
            df_subj = pd.DataFrame({
                "Subject": list(s_counts.keys()),
                "Total Tasks": list(s_counts.values()),
            })
            st.caption("Total Tasks by Subject")
            st.bar_chart(df_subj.set_index("Subject"), height=180)