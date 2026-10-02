# =========================================================
# MY TASKS
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


def render(app):

    st.title("📝 My Tasks")

    st.write(
        "View and manage all your academic tasks."
    )

    st.divider()

    if not app.student.tasks:

        st.info(
            "💗 No tasks yet. Go to 'Add Task' "
            "to create your first task."
        )

    else:

        for index, task in enumerate(
            app.student.tasks
        ):

            st.markdown(
                '<div class="task-card">',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(
                [3, 2, 1]
            )

            with col1:

                if task.completed:

                    st.markdown(
                        f"### ✅ {task.name}"
                    )

                else:

                    st.markdown(
                        f"### 📌 {task.name}"
                    )

                st.write(
                    f"**Subject:** {task.subject}"
                )

            with col2:

                st.write(
                    f"**Priority:** "
                    f"{task.priority}"
                )

                st.write(
                    f"**Deadline:** "
                    f"{task.deadline}"
                )

                st.write(
                    f"**Study Time:** "
                    f"{task.estimated_hours} hour(s)"
                )

            with col3:

                if task.completed:

                    st.success(
                        "Completed"
                    )

                else:

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{index}"
                    ):

                        app.complete_task(index)

                        st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )
