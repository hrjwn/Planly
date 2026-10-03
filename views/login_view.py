import streamlit as st
from models.student import Student
from controllers.student_controllers import StudentController
from controllers.task_controllers import TaskController
from controllers.focus_controllers import FocusController
from services.workload_analyzer import WorkloadAnalyzer

def render_profile_view(student: Student):
    st.markdown(
        """
        <div style="margin-bottom: 1.2rem;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #3B3036; margin-bottom: 0.2rem;">
                Student Profile
            </h1>
            <p style="font-size: 0.95rem; color: #8A737D; margin: 0;">
                Manage your academic credentials and system profile information.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tasks = TaskController.get_student_tasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks)
    focus_summary = FocusController.get_weekly_focus_summary(student.student_id)

    total_tasks = analysis["total_tasks"]
    completed_tasks = analysis["completed_tasks"]
    workload = analysis["workload_level"]
    focus_time = focus_summary["formatted_total_time"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Total Tasks</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{total_tasks}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Assignments</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Completed</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #C95A8D; margin: 0.2rem 0;">{completed_tasks}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Submitted work</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Workload Level</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D96C9D; margin: 0.2rem 0;">{workload}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Current pacing</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;">Focus Time</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #3B3036; margin: 0.2rem 0;">{focus_time}</div>
                <div style="font-size: 0.78rem; color: #8A737D;">Lifetime study</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown(
            """
            <div style="font-size: 1.1rem; font-weight: 600; color: #3B3036; margin-bottom: 0.6rem;">
                Edit Academic Information
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form(key="edit_profile_form"):
            new_name = st.text_input("Full Name", value=student.name)
            new_course = st.text_input("Course / Degree Program / Grade Level", value=student.course)

            st.text_input(
                "Email Address",
                value=student.email,
                disabled=True,
                help="Your login email is managed through authentication security and cannot be changed here.",
            )

            save_btn = st.form_submit_button(
                "Save Profile Changes", type="primary", use_container_width=True
            )

            if save_btn:
                ok, msg = StudentController.update_student_profile(
                    student, new_name, new_course
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with col_right:
        st.markdown(
            """
            <div style="font-size: 1.1rem; font-weight: 600; color: #3B3036; margin-bottom: 0.6rem;">
                Account & Security
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; padding: 1.3rem; border-radius: 14px; border: 1px solid #F3B6CF; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); font-size: 0.88rem; color: #3B3036; line-height: 1.6;">
                <div style="margin-bottom: 0.8rem;">
                    <b style="color: #D96C9D;">Authentication Provider</b><br>
                    <span style="color: #8A737D;">Supabase Authentication</span>
                </div>
                <div style="margin-bottom: 0.8rem;">
                    <b style="color: #D96C9D;">Data Isolation & Security</b><br>
                    <span style="color: #8A737D;">Enforced by PostgreSQL Row Level Security (RLS). Each student only has access to their own academic records.</span>
                </div>
                <div>
                    <b style="color: #D96C9D;">Password Protection</b><br>
                    <span style="color: #8A737D;">Passwords are securely encrypted through Supabase Auth and never stored in plain text.</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )