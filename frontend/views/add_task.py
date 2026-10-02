# =========================================================
# ADD TASK
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st
from datetime import date


def render(app):

    st.title("➕ Add a New Task")

    st.write(
        "Add your academic task and let Planly help "
        "you organize your workload."
    )

    st.divider()

    with st.form("add_task_form"):

        task_name = st.text_input(
            "📚 Task Name",
            placeholder="Example: Research Paper"
        )

        subject = st.text_input(
            "📖 Subject / Course",
            placeholder="Example: Computer Science"
        )

        priority = st.selectbox(
            "💗 Priority",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        deadline = st.date_input(
            "📅 Deadline",
            min_value=date.today()
        )

        estimated_hours = st.number_input(
            "⏰ Estimated Study Time (hours)",
            min_value=0.5,
            max_value=24.0,
            value=1.0,
            step=0.5
        )

        st.write("")

        submitted = st.form_submit_button(
            "🎀 Add Task"
        )

        if submitted:

            if not task_name.strip():

                st.error(
                    "Please enter a task name."
                )

            elif not subject.strip():

                st.error(
                    "Please enter a subject."
                )

            else:

                app.add_task(
                    task_name,
                    subject,
                    priority,
                    deadline,
                    estimated_hours
                )

                st.success(
                    f"🎀 '{task_name}' has been added to Planly!"
                )
