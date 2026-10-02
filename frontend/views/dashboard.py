# =========================================================
# DASHBOARD
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


def render(app):

    st.markdown(
        '<div class="planly-title">'
        'Welcome to Planly 🎀'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="planly-subtitle">'
        'Stay organized, manage your workload, '
        'and study at your own pace. 💗'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------------------
    # STATISTICS
    # ---------------------------------------------

    total_tasks = len(
        app.student.tasks
    )

    pending_tasks = len(
        app.student.get_pending_tasks()
    )

    completed_tasks = len(
        app.student.get_completed_tasks()
    )

    score = app.analyzer.calculate_score(
        app.student
    )

    workload = app.analyzer.get_workload_level(
        score
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Tasks",
            total_tasks
        )

    with col2:
        st.metric(
            "📌 Pending",
            pending_tasks
        )

    with col3:
        st.metric(
            "✅ Completed",
            completed_tasks
        )

    with col4:
        st.metric(
            "💗 Workload",
            workload
        )

    st.divider()

    # ---------------------------------------------
    # WORKLOAD MESSAGE
    # ---------------------------------------------

    st.subheader("💗 Your Current Workload")

    message = app.analyzer.get_workload_message(
        workload
    )

    if workload == "LOW":

        st.success(message)

    elif workload == "MODERATE":

        st.warning(message)

    else:

        st.error(message)

    st.markdown(
        f"""
        <div class="pink-card">
            <strong>Workload Balance Score</strong>
            <h2>{score}</h2>
            <p>
            This score is based on task priority,
            deadline proximity, and estimated study time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            Made with 💗 for students who want to stay organized.
        </div>
        """,
        unsafe_allow_html=True
    )
