import streamlit as st
from models.student import Student
from controllers.student_controller import StudentController
from controllers.task_controller import TaskController
from services.workload_analyzer import WorkloadAnalyzer
from ui.components import html, page_header, section_title, stat_card


def render_profile_view(student: Student):
    page_header(
        "Student Profile",
        "Manage your academic credentials and system profile information.",
    )

    tasks = TaskController.get_student_tasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks)
    total_tasks = analysis["total_tasks"]
    completed_tasks = analysis["completed_tasks"]
    workload = analysis["workload_level"]

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Total Tasks Tracked", total_tasks, "Academic assignments")
    with c2:
        stat_card("Completed Tasks", completed_tasks, "Successfully finished", "#C95A8D")
    with c3:
        stat_card("Current Workload", workload, "Active academic load", "#D96C9D")

    st.write("")

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        section_title("Edit Academic Information", size="1.1rem", margin="0 0 0.6rem 0")

        with st.form(key="edit_profile_form"):
            new_name = st.text_input("Full Name", value=student.name)
            new_course = st.text_input("Course / Degree Program", value=student.course)

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
        section_title("Account & Security", size="1.1rem", margin="0 0 0.6rem 0")
        html(
            """
            <div style="background-color: #FFFFFF; padding: 1.3rem; border-radius: 14px; border: 1px solid #F3B6CF; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); font-size: 0.88rem; color: #3B3036; line-height: 1.6;">
                <div style="margin-bottom: 0.8rem;">
                    <b style="color: #D96C9D;">Authentication Provider</b><br>
                    <span style="color: #8A737D;">Supabase Authentication (Cloud Auth)</span>
                </div>
                <div style="margin-bottom: 0.8rem;">
                    <b style="color: #D96C9D;">Data Isolation & Security</b><br>
                    <span style="color: #8A737D;">Enforced by PostgreSQL Row Level Security (RLS). Each student only has access to their own academic records.</span>
                </div>
                <div>
                    <b style="color: #D96C9D;">Password Protection</b><br>
                    <span style="color: #8A737D;">Passwords are securely hashed within Supabase Auth and never stored directly in the students database table.</span>
                </div>
            </div>
            """
        )