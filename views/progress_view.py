from datetime import date, datetime, timedelta
import streamlit as st
import pandas as pd
from models.student import Student
from controllers.task_controllers import TaskController
from services.workload_analyzer import WorkloadAnalyzer
from services.recommendation_service import RecommendationService


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
    deadlines_this_week = 0
    for t in upcoming:
        try:
            d_date = datetime.strptime(t.deadline, "%Y-%m-%d").date()
            if today <= d_date <= one_week_later:
                deadlines_this_week += 1
        except Exception:
            pass

    st.markdown(
        """
        <div style="margin-bottom: 1.2rem;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #3B3036; margin-bottom: 0.2rem;">
                My Progress
            </h1>
            <p style="font-size: 0.95rem; color: #8A737D; margin: 0;">
                Track your semester momentum, workload balance, and academic task completion.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )

    st.progress(pct / 100.0 if total > 0 else 0.0)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Total Tasks</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{total}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Semester assignments</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Completed Tasks</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #C95A8D; margin: 0.2rem 0;">{completed}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Submitted work</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Pending Tasks</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{pending}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Active workload</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Completion Rate</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{pct}%</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Overall completion</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 600; color: #3B3036; margin-top: 1rem; margin-bottom: 0.6rem;">
            Study Suggestions
        </div>
        """,
        unsafe_allow_html=True,
    )

    primary_advice = RecommendationService.get_primary_recommendation(workload)
    detailed_tips = RecommendationService.get_detailed_recommendations(analysis)

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )

    col_timeline, col_charts = st.columns([1.1, 0.9])

    with col_timeline:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.7rem;">
                Timeline: Upcoming Deadlines
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not upcoming:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                    No pending deadlines. Excellent job managing your assignments!
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for task in upcoming:
                days_left = task.days_until_deadline()

                if days_left < 0:
                    badge_str = f"Overdue by {abs(days_left)} days"
                    badge_style = "background-color: #FEE2E2; color: #B91C1C;"
                elif days_left == 0:
                    badge_str = "Due Today"
                    badge_style = "background-color: #FEF3C7; color: #B45309;"
                elif days_left == 1:
                    badge_str = "Due Tomorrow"
                    badge_style = "background-color: #FEF3C7; color: #B45309;"
                else:
                    badge_str = f"Due in {days_left} days"
                    badge_style = "background-color: #FCE8F0; color: #C95A8D;"

                st.markdown(
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
                    """,
                    unsafe_allow_html=True,
                )

    with col_charts:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.7rem;">
                Task Breakdown
            </div>
            """,
            unsafe_allow_html=True,
        )

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