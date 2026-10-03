from datetime import date, datetime, timedelta
import streamlit as st
import pandas as pd
from models.student import Student
from controllers.task_controllers import TaskController
from controllers.focus_controllers import FocusController
from services.workload_analyzer import WorkloadAnalyzer
from services.study_scheduler import StudyScheduler

def render_progress_view(student: Student):
    tasks = TaskController.get_student_tasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks)
    focus_summary = FocusController.get_weekly_focus_summary(student.student_id)

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
                Plan your work. Track your progress.
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
                        OVERALL PROGRESS
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

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

    with col_m1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">TOTAL TASKS</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{total}</div>
                <div style="font-size: 0.75rem; color: #8A737D;">Assignments</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_m2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">COMPLETED</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #C95A8D; margin: 0.2rem 0;">{completed}</div>
                <div style="font-size: 0.75rem; color: #8A737D;">Submitted</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_m3:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">PENDING</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{pending}</div>
                <div style="font-size: 0.75rem; color: #8A737D;">In progress</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_m4:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">FOCUS SESSIONS</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{focus_summary['weekly_sessions']}</div>
                <div style="font-size: 0.75rem; color: #8A737D;">This week</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_m5:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">FOCUS TIME</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{focus_summary['formatted_weekly_time']}</div>
                <div style="font-size: 0.75rem; color: #8A737D;">This week</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col_subj, col_sched = st.columns([1, 1.3])

    with col_subj:
        st.markdown(
            """
            <div style="font-size: 1.15rem; font-weight: 700; color: #3B3036; margin-bottom: 0.7rem;">
                Subject Progress
            </div>
            """,
            unsafe_allow_html=True,
        )

        subject_progress = analysis["subject_progress"]

        if not subject_progress:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                    No subject data available. Add tasks with subject categories to view your breakdown.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for subj_name, stats in subject_progress.items():
                s_total = stats["total"]
                s_comp = stats["completed"]
                s_ratio = stats["percentage"] / 100.0

                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.7rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.3rem;">
                            <div style="font-weight: 700; color: #3B3036; font-size: 0.95rem;">{subj_name}</div>
                            <div style="font-size: 0.8rem; color: #D96C9D; font-weight: 600;">{stats['percentage']}%</div>
                        </div>
                        <div style="font-size: 0.82rem; color: #8A737D; margin-bottom: 0.5rem;">
                            {s_total} task{'s' if s_total != 1 else ''} • {s_comp} completed
                        </div>
                        <div style="width: 100%; height: 6px; background-color: #FFF7FA; border: 1px solid #F3B6CF; border-radius: 8px; overflow: hidden;">
                            <div style="width: {int(s_ratio * 100)}%; height: 100%; background-color: #D96C9D;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col_sched:
        st.markdown(
            """
            <div style="font-size: 1.15rem; font-weight: 700; color: #3B3036; margin-bottom: 0.7rem;">
                Study Schedule Recommendations
            </div>
            """,
            unsafe_allow_html=True,
        )

        schedule_data = StudyScheduler.create_schedule(tasks, workload)
        task_schedules = schedule_data["task_schedules"]
        general_tips = schedule_data["general_tips"]

        if not task_schedules:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                    No pending tasks to schedule. You are fully caught up with your academic deadlines!
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for item in task_schedules[:3]:
                t = item["task"]
                steps = item["schedule"]
                deadline_label = t.get_deadline_label()

                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.7rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span style="font-weight: 700; color: #3B3036; font-size: 0.92rem;">{t.title}</span>
                            <span style="background-color: #FCE8F0; color: #C95A8D; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{deadline_label}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: #8A737D; margin-bottom: 0.5rem;">Subject: {t.subject} | Priority: <b>{t.priority}</b></div>
                        <div style="border-top: 1px solid #FFF7FA; padding-top: 0.4rem;">
                            {''.join(f'<div style="font-size: 0.82rem; margin-bottom: 0.25rem;"><b style="color: #D96C9D;">{step["day"]}:</b> <span style="color: #3B3036;">{step["activity"]}</span></div>' for step in steps)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if general_tips:
            st.markdown(
                f"""
                <div style="background-color: #FFF7FA; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.8rem;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.3rem;">
                        Workload Pacing Strategy
                    </div>
                    <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.82rem; color: #3B3036; line-height: 1.6;">
                        {''.join(f'<li style="margin-bottom: 0.25rem;">{tip}</li>' for tip in general_tips[:3])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.6rem;">
                Pending Tasks by Priority
            </div>
            """,
            unsafe_allow_html=True,
        )
        p_counts = analysis["tasks_by_priority"]
        df_priority = pd.DataFrame({
            "Priority": list(p_counts.keys()),
            "Pending Tasks": list(p_counts.values()),
        })
        st.bar_chart(df_priority.set_index("Priority"), height=190)

    with col_c2:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin-bottom: 0.6rem;">
                Total Tasks by Subject
            </div>
            """,
            unsafe_allow_html=True,
        )
        s_counts = analysis["tasks_by_subject"]
        if s_counts:
            df_subj = pd.DataFrame({
                "Subject": list(s_counts.keys()),
                "Total Tasks": list(s_counts.values()),
            })
            st.bar_chart(df_subj.set_index("Subject"), height=190)
        else:
            st.caption("No subjects tracked yet.")